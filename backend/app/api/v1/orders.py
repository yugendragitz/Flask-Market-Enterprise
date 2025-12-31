"""
FlaskMarket Enterprise - Orders API
Order creation, checkout, and order management
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import desc
from app.api.v1 import api_v1_bp
from app.extensions import db
from app.models import Order, OrderItem, CartItem, Transaction, Coupon


@api_v1_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    """
    Get user's orders
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')
    
    query = current_user.orders
    
    if status:
        query = query.filter(Order.status == status)
    
    pagination = query.order_by(desc(Order.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': {
            'orders': [order.to_dict() for order in pagination.items],
            'pagination': {
                'page': pagination.page,
                'total_pages': pagination.pages,
                'total_items': pagination.total
            }
        }
    })


@api_v1_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """
    Get single order details
    """
    order = Order.query.filter_by(
        id=order_id, user_id=current_user.id
    ).first_or_404()
    
    return jsonify({
        'success': True,
        'data': {
            'order': order.to_dict(include_items=True)
        }
    })


@api_v1_bp.route('/orders/checkout', methods=['POST'])
@jwt_required()
def checkout():
    """
    Process checkout and create order
    ---
    Request Body:
        - shipping_address: object (required)
        - payment_method: string (default: 'wallet')
        - coupon_code: string (optional)
        - customer_notes: string (optional)
    """
    data = request.get_json()
    
    # Get cart items
    cart_items = current_user.cart_items.all()
    
    if not cart_items:
        return jsonify({
            'success': False,
            'message': 'Your cart is empty'
        }), 400
    
    # Validate shipping address
    shipping_address = data.get('shipping_address')
    if not shipping_address:
        return jsonify({
            'success': False,
            'message': 'Shipping address is required'
        }), 400
    
    required_address_fields = ['full_name', 'phone', 'address_line1', 'city', 'state', 'postal_code']
    for field in required_address_fields:
        if not shipping_address.get(field):
            return jsonify({
                'success': False,
                'message': f'{field} is required in shipping address'
            }), 400
    
    # Calculate totals
    subtotal = sum(item.subtotal for item in cart_items)
    shipping_cost = 0 if subtotal >= 500 else 50
    tax_amount = round(subtotal * 0.18, 2)  # 18% GST
    discount_amount = 0
    
    # Apply coupon if provided
    coupon_code = data.get('coupon_code')
    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code.upper()).first()
        if coupon:
            is_valid, message = coupon.is_valid()
            if is_valid:
                discount_amount = coupon.calculate_discount(subtotal)
                coupon.used_count += 1
            else:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
    
    total_amount = subtotal - discount_amount + shipping_cost + tax_amount
    
    # Check wallet balance
    if data.get('payment_method', 'wallet') == 'wallet':
        if not current_user.can_afford(total_amount):
            return jsonify({
                'success': False,
                'message': f'Insufficient wallet balance. You need ${total_amount:.2f} but have {current_user.formatted_balance}'
            }), 400
    
    try:
        # Create order
        order = Order(
            order_number=Order.generate_order_number(),
            user_id=current_user.id,
            subtotal=subtotal,
            discount_amount=discount_amount,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            total_amount=total_amount,
            payment_method=data.get('payment_method', 'wallet'),
            shipping_address=shipping_address,
            customer_notes=data.get('customer_notes'),
            status='confirmed',
            payment_status='paid'
        )
        
        db.session.add(order)
        
        # Create order items
        for cart_item in cart_items:
            product = cart_item.product
            
            # Check stock again
            if product.track_inventory and product.stock_quantity < cart_item.quantity:
                db.session.rollback()
                return jsonify({
                    'success': False,
                    'message': f'{product.name} has insufficient stock'
                }), 400
            
            order_item = OrderItem(
                order=order,
                product_id=product.id,
                product_name=product.name,
                product_sku=product.sku,
                product_image=product.thumbnail_url,
                quantity=cart_item.quantity,
                unit_price=product.price
            )
            
            db.session.add(order_item)
            
            # Decrease stock
            product.decrement_stock(cart_item.quantity)
        
        # Deduct wallet balance
        balance_before = current_user.wallet_balance
        current_user.deduct_balance(total_amount)
        
        # Create transaction record
        transaction = Transaction(
            transaction_id=Transaction.generate_transaction_id(),
            user_id=current_user.id,
            order_id=order.id,
            transaction_type='purchase',
            amount=total_amount,
            balance_before=balance_before,
            balance_after=current_user.wallet_balance,
            status='completed',
            description=f'Purchase: Order {order.order_number}'
        )
        
        db.session.add(transaction)
        
        # Clear cart
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order placed successfully!',
            'data': {
                'order': order.to_dict(include_items=True),
                'wallet_balance': current_user.formatted_balance
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to process order',
            'error': str(e)
        }), 500


@api_v1_bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_order(order_id):
    """
    Cancel an order (only if not shipped)
    """
    order = Order.query.filter_by(
        id=order_id, user_id=current_user.id
    ).first_or_404()
    
    # Check if order can be cancelled
    if order.status in ['shipped', 'delivered', 'cancelled']:
        return jsonify({
            'success': False,
            'message': f'Order cannot be cancelled. Current status: {order.status}'
        }), 400
    
    try:
        # Restore stock
        for item in order.items:
            if item.product:
                item.product.increment_stock(item.quantity)
        
        # Refund to wallet
        balance_before = current_user.wallet_balance
        current_user.add_balance(order.total_amount)
        
        # Create refund transaction
        transaction = Transaction(
            transaction_id=Transaction.generate_transaction_id(),
            user_id=current_user.id,
            order_id=order.id,
            transaction_type='refund',
            amount=order.total_amount,
            balance_before=balance_before,
            balance_after=current_user.wallet_balance,
            status='completed',
            description=f'Refund: Order {order.order_number} cancelled'
        )
        
        db.session.add(transaction)
        
        # Update order status
        order.status = 'cancelled'
        order.payment_status = 'refunded'
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order cancelled and refunded successfully',
            'data': {
                'order': order.to_dict(),
                'refund_amount': order.total_amount,
                'wallet_balance': current_user.formatted_balance
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Failed to cancel order',
            'error': str(e)
        }), 500


@api_v1_bp.route('/orders/validate-coupon', methods=['POST'])
@jwt_required()
def validate_coupon():
    """
    Validate a coupon code
    """
    data = request.get_json()
    code = data.get('code', '').upper().strip()
    
    if not code:
        return jsonify({
            'success': False,
            'message': 'Coupon code is required'
        }), 400
    
    coupon = Coupon.query.filter_by(code=code).first()
    
    if not coupon:
        return jsonify({
            'success': False,
            'message': 'Invalid coupon code'
        }), 404
    
    is_valid, message = coupon.is_valid()
    
    if not is_valid:
        return jsonify({
            'success': False,
            'message': message
        }), 400
    
    # Calculate discount based on cart
    cart_subtotal = sum(item.subtotal for item in current_user.cart_items)
    
    if cart_subtotal < coupon.min_order_amount:
        return jsonify({
            'success': False,
            'message': f'Minimum order amount is ${coupon.min_order_amount}'
        }), 400
    
    discount = coupon.calculate_discount(cart_subtotal)
    
    return jsonify({
        'success': True,
        'message': 'Coupon applied successfully',
        'data': {
            'coupon': coupon.to_dict(),
            'discount_amount': discount
        }
    })


@api_v1_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_transactions():
    """
    Get user's transaction history
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = Transaction.query.filter_by(user_id=current_user.id).order_by(
        desc(Transaction.created_at)
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'data': {
            'transactions': [t.to_dict() for t in pagination.items],
            'pagination': {
                'page': pagination.page,
                'total_pages': pagination.pages,
                'total_items': pagination.total
            }
        }
    })
