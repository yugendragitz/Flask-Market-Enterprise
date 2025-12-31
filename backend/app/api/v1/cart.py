"""
FlaskMarket Enterprise - Cart API
Shopping cart operations
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.api.v1 import api_v1_bp
from app.extensions import db
from app.models import CartItem, Product


@api_v1_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    """
    Get user's shopping cart
    """
    cart_items = current_user.cart_items.all()
    
    subtotal = sum(item.subtotal for item in cart_items)
    item_count = sum(item.quantity for item in cart_items)
    
    return jsonify({
        'success': True,
        'data': {
            'items': [item.to_dict() for item in cart_items],
            'summary': {
                'item_count': item_count,
                'subtotal': subtotal,
                'shipping': 0 if subtotal >= 500 else 50,  # Free shipping over $500
                'tax': round(subtotal * 0.18, 2),  # 18% GST
                'total': round(subtotal + (0 if subtotal >= 500 else 50) + (subtotal * 0.18), 2)
            }
        }
    })


@api_v1_bp.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """
    Add item to cart
    ---
    Request Body:
        - product_id: int (required)
        - quantity: int (default: 1)
    """
    data = request.get_json()
    
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if not product_id:
        return jsonify({
            'success': False,
            'message': 'Product ID is required'
        }), 400
    
    if quantity < 1:
        return jsonify({
            'success': False,
            'message': 'Quantity must be at least 1'
        }), 400
    
    # Check product exists and is available
    product = Product.query.get_or_404(product_id)
    
    if not product.is_active:
        return jsonify({
            'success': False,
            'message': 'Product is not available'
        }), 400
    
    if product.track_inventory and product.stock_quantity < quantity:
        return jsonify({
            'success': False,
            'message': f'Only {product.stock_quantity} items available in stock'
        }), 400
    
    # Check if item already in cart
    cart_item = CartItem.query.filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()
    
    if cart_item:
        # Update quantity
        new_quantity = cart_item.quantity + quantity
        if product.track_inventory and product.stock_quantity < new_quantity:
            return jsonify({
                'success': False,
                'message': f'Cannot add more. Only {product.stock_quantity} items available'
            }), 400
        
        cart_item.quantity = new_quantity
    else:
        # Create new cart item
        cart_item = CartItem(
            user_id=current_user.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    
    # Get updated cart count
    cart_count = sum(item.quantity for item in current_user.cart_items)
    
    return jsonify({
        'success': True,
        'message': f'{product.name} added to cart',
        'data': {
            'cart_item': cart_item.to_dict(),
            'cart_count': cart_count
        }
    })


@api_v1_bp.route('/cart/update/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    """
    Update cart item quantity
    ---
    Request Body:
        - quantity: int (required)
    """
    cart_item = CartItem.query.filter_by(
        id=item_id, user_id=current_user.id
    ).first_or_404()
    
    data = request.get_json()
    quantity = data.get('quantity')
    
    if quantity is None or quantity < 0:
        return jsonify({
            'success': False,
            'message': 'Valid quantity is required'
        }), 400
    
    if quantity == 0:
        # Remove item
        db.session.delete(cart_item)
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Item removed from cart'
        })
    
    # Check stock
    product = cart_item.product
    if product.track_inventory and product.stock_quantity < quantity:
        return jsonify({
            'success': False,
            'message': f'Only {product.stock_quantity} items available'
        }), 400
    
    cart_item.quantity = quantity
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cart updated',
        'data': {
            'cart_item': cart_item.to_dict()
        }
    })


@api_v1_bp.route('/cart/remove/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(item_id):
    """
    Remove item from cart
    """
    cart_item = CartItem.query.filter_by(
        id=item_id, user_id=current_user.id
    ).first_or_404()
    
    product_name = cart_item.product.name
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{product_name} removed from cart'
    })


@api_v1_bp.route('/cart/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """
    Clear entire cart
    """
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Cart cleared'
    })


@api_v1_bp.route('/cart/count', methods=['GET'])
@jwt_required()
def get_cart_count():
    """
    Get cart item count (for header badge)
    """
    count = sum(item.quantity for item in current_user.cart_items)
    
    return jsonify({
        'success': True,
        'data': {
            'count': count
        }
    })
