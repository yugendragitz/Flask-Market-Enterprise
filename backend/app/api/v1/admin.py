"""
FlaskMarket Enterprise - Admin API
Admin-only operations for managing products, users, orders
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from app.api.v1 import api_v1_bp
from app.extensions import db
from app.models import Product, Category, ProductImage, User, Order, Transaction, Coupon
from app.utils.decorators import admin_required
from app.utils.helpers import generate_slug


# ============ Dashboard ============

@api_v1_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@admin_required
def admin_dashboard():
    """
    Get admin dashboard statistics
    """
    # Time ranges
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Total counts
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    
    # Revenue calculations
    total_revenue = db.session.query(func.sum(Order.total_amount)).filter(
        Order.payment_status == 'paid'
    ).scalar() or 0
    
    monthly_revenue = db.session.query(func.sum(Order.total_amount)).filter(
        Order.payment_status == 'paid',
        Order.created_at >= month_ago
    ).scalar() or 0
    
    # Recent orders
    recent_orders = Order.query.order_by(desc(Order.created_at)).limit(5).all()
    
    # Order status breakdown
    order_status_counts = db.session.query(
        Order.status, func.count(Order.id)
    ).group_by(Order.status).all()
    
    # Low stock products
    low_stock_products = Product.query.filter(
        Product.track_inventory == True,
        Product.stock_quantity <= Product.low_stock_threshold
    ).limit(10).all()
    
    # Top selling products
    top_products = Product.query.order_by(desc(Product.sold_count)).limit(5).all()
    
    return jsonify({
        'success': True,
        'data': {
            'stats': {
                'total_users': total_users,
                'total_products': total_products,
                'total_orders': total_orders,
                'total_revenue': total_revenue,
                'monthly_revenue': monthly_revenue
            },
            'order_status_breakdown': dict(order_status_counts),
            'recent_orders': [o.to_dict() for o in recent_orders],
            'low_stock_products': [p.to_dict() for p in low_stock_products],
            'top_selling_products': [p.to_dict() for p in top_products]
        }
    })


# ============ Product Management ============

@api_v1_bp.route('/admin/products', methods=['POST'])
@jwt_required()
@admin_required
def create_product():
    """
    Create a new product
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'price', 'description']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'success': False,
                'message': f'{field} is required'
            }), 400
    
    # Generate slug and SKU
    slug = generate_slug(data['name'])
    sku = data.get('sku') or f"SKU-{slug[:8].upper()}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    
    # Check if slug already exists
    if Product.query.filter_by(slug=slug).first():
        slug = f"{slug}-{datetime.utcnow().strftime('%H%M%S')}"
    
    product = Product(
        name=data['name'],
        slug=slug,
        sku=sku,
        barcode=data.get('barcode'),
        short_description=data.get('short_description'),
        description=data['description'],
        specifications=data.get('specifications'),
        price=data['price'],
        compare_price=data.get('compare_price'),
        cost_price=data.get('cost_price'),
        stock_quantity=data.get('stock_quantity', 0),
        low_stock_threshold=data.get('low_stock_threshold', 10),
        track_inventory=data.get('track_inventory', True),
        thumbnail_url=data.get('thumbnail_url'),
        brand=data.get('brand'),
        is_active=data.get('is_active', True),
        is_featured=data.get('is_featured', False),
        is_new=data.get('is_new', True)
    )
    
    # Add categories
    category_ids = data.get('category_ids', [])
    for cat_id in category_ids:
        category = Category.query.get(cat_id)
        if category:
            product.categories.append(category)
    
    db.session.add(product)
    db.session.commit()
    
    # Add images
    images = data.get('images', [])
    for i, img_url in enumerate(images):
        image = ProductImage(
            product_id=product.id,
            image_url=img_url,
            is_primary=(i == 0),
            display_order=i
        )
        db.session.add(image)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Product created successfully',
        'data': {
            'product': product.to_dict(include_details=True)
        }
    }), 201


@api_v1_bp.route('/admin/products/<int:product_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_product(product_id):
    """
    Update a product
    """
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    # Update fields
    allowed_fields = [
        'name', 'short_description', 'description', 'specifications',
        'price', 'compare_price', 'cost_price', 'stock_quantity',
        'low_stock_threshold', 'track_inventory', 'thumbnail_url',
        'brand', 'is_active', 'is_featured', 'is_new', 'barcode'
    ]
    
    for field in allowed_fields:
        if field in data:
            setattr(product, field, data[field])
    
    # Update slug if name changed
    if 'name' in data:
        product.slug = generate_slug(data['name'])
    
    # Update categories
    if 'category_ids' in data:
        product.categories.clear()
        for cat_id in data['category_ids']:
            category = Category.query.get(cat_id)
            if category:
                product.categories.append(category)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Product updated successfully',
        'data': {
            'product': product.to_dict(include_details=True)
        }
    })


@api_v1_bp.route('/admin/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_product(product_id):
    """
    Delete a product (soft delete by setting inactive)
    """
    product = Product.query.get_or_404(product_id)
    
    # Soft delete
    product.is_active = False
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Product deleted successfully'
    })


# ============ Category Management ============

@api_v1_bp.route('/admin/categories', methods=['POST'])
@jwt_required()
@admin_required
def create_category():
    """
    Create a new category
    """
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({
            'success': False,
            'message': 'Category name is required'
        }), 400
    
    slug = generate_slug(data['name'])
    
    if Category.query.filter_by(slug=slug).first():
        return jsonify({
            'success': False,
            'message': 'Category with this name already exists'
        }), 409
    
    category = Category(
        name=data['name'],
        slug=slug,
        description=data.get('description'),
        image_url=data.get('image_url'),
        icon=data.get('icon'),
        parent_id=data.get('parent_id'),
        display_order=data.get('display_order', 0)
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Category created successfully',
        'data': {
            'category': category.to_dict()
        }
    }), 201


@api_v1_bp.route('/admin/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_category(category_id):
    """
    Update a category
    """
    category = Category.query.get_or_404(category_id)
    data = request.get_json()
    
    if 'name' in data:
        category.name = data['name']
        category.slug = generate_slug(data['name'])
    
    if 'description' in data:
        category.description = data['description']
    
    if 'image_url' in data:
        category.image_url = data['image_url']
    
    if 'icon' in data:
        category.icon = data['icon']
    
    if 'is_active' in data:
        category.is_active = data['is_active']
    
    if 'display_order' in data:
        category.display_order = data['display_order']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Category updated successfully',
        'data': {
            'category': category.to_dict()
        }
    })


# ============ Order Management ============

@api_v1_bp.route('/admin/orders', methods=['GET'])
@jwt_required()
@admin_required
def admin_get_orders():
    """
    Get all orders with filters
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    status = request.args.get('status')
    
    query = Order.query
    
    if status:
        query = query.filter(Order.status == status)
    
    pagination = query.order_by(desc(Order.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': {
            'orders': [o.to_dict(include_items=True) for o in pagination.items],
            'pagination': {
                'page': pagination.page,
                'total_pages': pagination.pages,
                'total_items': pagination.total
            }
        }
    })


@api_v1_bp.route('/admin/orders/<int:order_id>/status', methods=['PUT'])
@jwt_required()
@admin_required
def update_order_status(order_id):
    """
    Update order status
    """
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    new_status = data.get('status')
    valid_statuses = ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']
    
    if new_status not in valid_statuses:
        return jsonify({
            'success': False,
            'message': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'
        }), 400
    
    order.status = new_status
    
    if new_status == 'shipped':
        order.shipped_at = datetime.utcnow()
    elif new_status == 'delivered':
        order.delivered_at = datetime.utcnow()
    
    if data.get('admin_notes'):
        order.admin_notes = data['admin_notes']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'Order status updated to {new_status}',
        'data': {
            'order': order.to_dict()
        }
    })


# ============ User Management ============

@api_v1_bp.route('/admin/users', methods=['GET'])
@jwt_required()
@admin_required
def admin_get_users():
    """
    Get all users
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    pagination = User.query.order_by(desc(User.created_at)).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'success': True,
        'data': {
            'users': [u.to_dict(include_private=True) for u in pagination.items],
            'pagination': {
                'page': pagination.page,
                'total_pages': pagination.pages,
                'total_items': pagination.total
            }
        }
    })


@api_v1_bp.route('/admin/users/<int:user_id>/toggle-active', methods=['PUT'])
@jwt_required()
@admin_required
def toggle_user_active(user_id):
    """
    Toggle user active status
    """
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({
            'success': False,
            'message': 'Cannot deactivate yourself'
        }), 400
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    
    return jsonify({
        'success': True,
        'message': f'User {status} successfully'
    })


# ============ Coupon Management ============

@api_v1_bp.route('/admin/coupons', methods=['GET'])
@jwt_required()
@admin_required
def get_coupons():
    """
    Get all coupons
    """
    coupons = Coupon.query.order_by(desc(Coupon.created_at)).all()
    
    return jsonify({
        'success': True,
        'data': {
            'coupons': [c.to_dict() for c in coupons]
        }
    })


@api_v1_bp.route('/admin/coupons', methods=['POST'])
@jwt_required()
@admin_required
def create_coupon():
    """
    Create a new coupon
    """
    data = request.get_json()
    
    if not data.get('code') or not data.get('discount_type') or not data.get('discount_value'):
        return jsonify({
            'success': False,
            'message': 'code, discount_type, and discount_value are required'
        }), 400
    
    code = data['code'].upper().strip()
    
    if Coupon.query.filter_by(code=code).first():
        return jsonify({
            'success': False,
            'message': 'Coupon code already exists'
        }), 409
    
    coupon = Coupon(
        code=code,
        discount_type=data['discount_type'],
        discount_value=data['discount_value'],
        min_order_amount=data.get('min_order_amount', 0),
        max_discount_amount=data.get('max_discount_amount'),
        usage_limit=data.get('usage_limit'),
        per_user_limit=data.get('per_user_limit', 1),
        expires_at=datetime.fromisoformat(data['expires_at']) if data.get('expires_at') else None
    )
    
    db.session.add(coupon)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Coupon created successfully',
        'data': {
            'coupon': coupon.to_dict()
        }
    }), 201
