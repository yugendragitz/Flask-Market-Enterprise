"""
FlaskMarket Enterprise - Product Model
Enterprise-grade product model with categories, variants, and inventory
"""

from datetime import datetime
from app.extensions import db


# Association table for product-category many-to-many
product_categories = db.Table('product_categories',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
)


class Category(db.Model):
    """Product category model"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    icon = db.Column(db.String(50))  # Font Awesome icon class
    
    # Parent category for nested categories
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    
    is_active = db.Column(db.Boolean, default=True)
    display_order = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self, include_children=False):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'image_url': self.image_url,
            'icon': self.icon,
            'is_active': self.is_active,
            'product_count': self.products.count() if hasattr(self, 'products') else 0
        }
        
        if include_children and self.children:
            data['children'] = [child.to_dict() for child in self.children]
        
        return data


class Product(db.Model):
    """Product model with comprehensive e-commerce features"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Info
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    barcode = db.Column(db.String(50), unique=True)
    
    # Description
    short_description = db.Column(db.String(500))
    description = db.Column(db.Text, nullable=False)
    specifications = db.Column(db.JSON)  # Store specs as JSON
    
    # Pricing
    price = db.Column(db.Float, nullable=False)
    compare_price = db.Column(db.Float)  # Original price for showing discount
    cost_price = db.Column(db.Float)  # Cost for profit calculation
    
    # Inventory
    stock_quantity = db.Column(db.Integer, default=0)
    low_stock_threshold = db.Column(db.Integer, default=10)
    track_inventory = db.Column(db.Boolean, default=True)
    
    # Media
    thumbnail_url = db.Column(db.String(500))
    
    # SEO
    meta_title = db.Column(db.String(200))
    meta_description = db.Column(db.String(500))
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_new = db.Column(db.Boolean, default=True)
    
    # Stats
    view_count = db.Column(db.Integer, default=0)
    sold_count = db.Column(db.Integer, default=0)
    
    # Brand
    brand = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    categories = db.relationship('Category', secondary=product_categories,
                                backref=db.backref('products', lazy='dynamic'))
    images = db.relationship('ProductImage', backref='product', lazy='dynamic',
                            cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy='dynamic',
                             cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.name}>'
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.compare_price and self.compare_price > self.price:
            return round(((self.compare_price - self.price) / self.compare_price) * 100)
        return 0
    
    @property
    def in_stock(self):
        """Check if product is in stock"""
        if not self.track_inventory:
            return True
        return self.stock_quantity > 0
    
    @property
    def low_stock(self):
        """Check if product is low on stock"""
        return self.track_inventory and self.stock_quantity <= self.low_stock_threshold
    
    @property
    def average_rating(self):
        """Calculate average rating from reviews"""
        reviews = self.reviews.all()
        if not reviews:
            return 0
        return round(sum(r.rating for r in reviews) / len(reviews), 1)
    
    @property
    def review_count(self):
        """Get total review count"""
        return self.reviews.count()
    
    def increment_view(self):
        """Increment view count"""
        self.view_count += 1
    
    def decrement_stock(self, quantity=1):
        """Decrease stock quantity"""
        if self.track_inventory:
            self.stock_quantity = max(0, self.stock_quantity - quantity)
            self.sold_count += quantity
    
    def increment_stock(self, quantity=1):
        """Increase stock quantity"""
        if self.track_inventory:
            self.stock_quantity += quantity
    
    def to_dict(self, include_details=False):
        """Serialize product to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'sku': self.sku,
            'short_description': self.short_description,
            'price': self.price,
            'compare_price': self.compare_price,
            'discount_percentage': self.discount_percentage,
            'thumbnail_url': self.thumbnail_url,
            'in_stock': self.in_stock,
            'stock_quantity': self.stock_quantity if self.track_inventory else None,
            'average_rating': self.average_rating,
            'review_count': self.review_count,
            'brand': self.brand,
            'is_featured': self.is_featured,
            'is_new': self.is_new,
            'categories': [cat.to_dict() for cat in self.categories]
        }
        
        if include_details:
            data.update({
                'description': self.description,
                'specifications': self.specifications,
                'barcode': self.barcode,
                'images': [img.to_dict() for img in self.images.all()],
                'view_count': self.view_count,
                'sold_count': self.sold_count,
                'created_at': self.created_at.isoformat() if self.created_at else None
            })
        
        return data


class ProductImage(db.Model):
    """Product image gallery"""
    __tablename__ = 'product_images'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    image_url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(200))
    is_primary = db.Column(db.Boolean, default=False)
    display_order = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'alt_text': self.alt_text,
            'is_primary': self.is_primary
        }


class Review(db.Model):
    """Product review model"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(200))
    comment = db.Column(db.Text)
    
    is_verified_purchase = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=True)
    helpful_count = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'is_verified_purchase': self.is_verified_purchase,
            'helpful_count': self.helpful_count,
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'avatar_url': self.user.avatar_url
            } if self.user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class WishlistItem(db.Model):
    """User wishlist"""
    __tablename__ = 'wishlist_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_wishlist_item'),
    )

