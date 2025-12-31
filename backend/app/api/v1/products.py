"""
FlaskMarket Enterprise - Products API
CRUD operations for products with filtering, searching, and pagination
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import or_, desc, asc
from app.api.v1 import api_v1_bp
from app.extensions import db
from app.models import Product, Category, Review, WishlistItem
from app.utils.decorators import admin_required


@api_v1_bp.route('/products', methods=['GET'])
def get_products():
    """
    Get all products with filtering, searching, and pagination
    ---
    Query Parameters:
        - page: int (default: 1)
        - per_page: int (default: 12, max: 100)
        - category: string (category slug)
        - search: string (search query)
        - min_price: float
        - max_price: float
        - brand: string
        - sort: string (price_asc, price_desc, newest, popular, rating)
        - in_stock: boolean
        - featured: boolean
    """
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 12, type=int), 100)
    
    # Build query
    query = Product.query.filter(Product.is_active == True)
    
    # Filter by category
    category_slug = request.args.get('category')
    if category_slug:
        category = Category.query.filter_by(slug=category_slug).first()
        if category:
            query = query.filter(Product.categories.contains(category))
    
    # Search
    search = request.args.get('search', '').strip()
    if search:
        search_term = f'%{search}%'
        query = query.filter(
            or_(
                Product.name.ilike(search_term),
                Product.description.ilike(search_term),
                Product.brand.ilike(search_term),
                Product.sku.ilike(search_term)
            )
        )
    
    # Price range
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Brand filter
    brand = request.args.get('brand')
    if brand:
        query = query.filter(Product.brand.ilike(f'%{brand}%'))
    
    # Stock filter
    in_stock = request.args.get('in_stock')
    if in_stock == 'true':
        query = query.filter(Product.stock_quantity > 0)
    
    # Featured filter
    featured = request.args.get('featured')
    if featured == 'true':
        query = query.filter(Product.is_featured == True)
    
    # Sorting
    sort = request.args.get('sort', 'newest')
    if sort == 'price_asc':
        query = query.order_by(asc(Product.price))
    elif sort == 'price_desc':
        query = query.order_by(desc(Product.price))
    elif sort == 'popular':
        query = query.order_by(desc(Product.sold_count))
    elif sort == 'rating':
        query = query.order_by(desc(Product.view_count))  # Placeholder
    else:  # newest
        query = query.order_by(desc(Product.created_at))
    
    # Paginate
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'success': True,
        'data': {
            'products': [p.to_dict() for p in pagination.items],
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total_pages': pagination.pages,
                'total_items': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        }
    })


@api_v1_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get single product by ID with full details
    """
    product = Product.query.get_or_404(product_id)
    
    # Increment view count
    product.increment_view()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': {
            'product': product.to_dict(include_details=True)
        }
    })


@api_v1_bp.route('/products/slug/<slug>', methods=['GET'])
def get_product_by_slug(slug):
    """
    Get product by slug
    """
    product = Product.query.filter_by(slug=slug, is_active=True).first_or_404()
    
    product.increment_view()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'data': {
            'product': product.to_dict(include_details=True)
        }
    })


@api_v1_bp.route('/products/featured', methods=['GET'])
def get_featured_products():
    """
    Get featured products for homepage
    """
    limit = request.args.get('limit', 8, type=int)
    products = Product.query.filter_by(
        is_active=True, is_featured=True
    ).order_by(desc(Product.created_at)).limit(limit).all()
    
    return jsonify({
        'success': True,
        'data': {
            'products': [p.to_dict() for p in products]
        }
    })


@api_v1_bp.route('/products/new', methods=['GET'])
def get_new_products():
    """
    Get new arrivals
    """
    limit = request.args.get('limit', 8, type=int)
    products = Product.query.filter_by(
        is_active=True, is_new=True
    ).order_by(desc(Product.created_at)).limit(limit).all()
    
    return jsonify({
        'success': True,
        'data': {
            'products': [p.to_dict() for p in products]
        }
    })


@api_v1_bp.route('/products/bestsellers', methods=['GET'])
def get_bestsellers():
    """
    Get bestselling products
    """
    limit = request.args.get('limit', 8, type=int)
    products = Product.query.filter_by(is_active=True).order_by(
        desc(Product.sold_count)
    ).limit(limit).all()
    
    return jsonify({
        'success': True,
        'data': {
            'products': [p.to_dict() for p in products]
        }
    })


# ============ Categories ============

@api_v1_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Get all categories
    """
    include_children = request.args.get('include_children', 'false') == 'true'
    
    # Get top-level categories
    categories = Category.query.filter_by(
        is_active=True, parent_id=None
    ).order_by(Category.display_order).all()
    
    return jsonify({
        'success': True,
        'data': {
            'categories': [c.to_dict(include_children=include_children) for c in categories]
        }
    })


@api_v1_bp.route('/categories/<slug>', methods=['GET'])
def get_category(slug):
    """
    Get category by slug
    """
    category = Category.query.filter_by(slug=slug, is_active=True).first_or_404()
    
    return jsonify({
        'success': True,
        'data': {
            'category': category.to_dict(include_children=True)
        }
    })


# ============ Reviews ============

@api_v1_bp.route('/products/<int:product_id>/reviews', methods=['GET'])
def get_product_reviews(product_id):
    """
    Get reviews for a product
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    product = Product.query.get_or_404(product_id)
    
    pagination = product.reviews.filter_by(is_approved=True).order_by(
        desc(Review.created_at)
    ).paginate(page=page, per_page=per_page, error_out=False)
    
    # Calculate rating distribution
    all_reviews = product.reviews.filter_by(is_approved=True).all()
    rating_distribution = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for review in all_reviews:
        rating_distribution[review.rating] += 1
    
    return jsonify({
        'success': True,
        'data': {
            'reviews': [r.to_dict() for r in pagination.items],
            'average_rating': product.average_rating,
            'total_reviews': product.review_count,
            'rating_distribution': rating_distribution,
            'pagination': {
                'page': pagination.page,
                'total_pages': pagination.pages,
                'total_items': pagination.total
            }
        }
    })


@api_v1_bp.route('/products/<int:product_id>/reviews', methods=['POST'])
@jwt_required()
def create_review(product_id):
    """
    Create a review for a product
    """
    product = Product.query.get_or_404(product_id)
    data = request.get_json()
    
    # Check if user already reviewed this product
    existing_review = Review.query.filter_by(
        product_id=product_id, user_id=current_user.id
    ).first()
    
    if existing_review:
        return jsonify({
            'success': False,
            'message': 'You have already reviewed this product'
        }), 400
    
    # Validate rating
    rating = data.get('rating')
    if not rating or rating < 1 or rating > 5:
        return jsonify({
            'success': False,
            'message': 'Rating must be between 1 and 5'
        }), 400
    
    review = Review(
        product_id=product_id,
        user_id=current_user.id,
        rating=rating,
        title=data.get('title'),
        comment=data.get('comment')
    )
    
    db.session.add(review)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Review submitted successfully',
        'data': {
            'review': review.to_dict()
        }
    }), 201


# ============ Wishlist ============

@api_v1_bp.route('/wishlist', methods=['GET'])
@jwt_required()
def get_wishlist():
    """
    Get user's wishlist
    """
    wishlist = current_user.wishlist.all()
    
    return jsonify({
        'success': True,
        'data': {
            'wishlist': [{
                'id': item.id,
                'product': item.product.to_dict(),
                'added_at': item.created_at.isoformat()
            } for item in wishlist]
        }
    })


@api_v1_bp.route('/wishlist/<int:product_id>', methods=['POST'])
@jwt_required()
def add_to_wishlist(product_id):
    """
    Add product to wishlist
    """
    product = Product.query.get_or_404(product_id)
    
    # Check if already in wishlist
    existing = WishlistItem.query.filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()
    
    if existing:
        return jsonify({
            'success': False,
            'message': 'Product already in wishlist'
        }), 400
    
    wishlist_item = WishlistItem(
        user_id=current_user.id,
        product_id=product_id
    )
    
    db.session.add(wishlist_item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Added to wishlist'
    }), 201


@api_v1_bp.route('/wishlist/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(product_id):
    """
    Remove product from wishlist
    """
    wishlist_item = WishlistItem.query.filter_by(
        user_id=current_user.id, product_id=product_id
    ).first_or_404()
    
    db.session.delete(wishlist_item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Removed from wishlist'
    })
