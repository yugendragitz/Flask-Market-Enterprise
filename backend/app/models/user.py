"""
FlaskMarket Enterprise - User Model
Enterprise-grade user model with role-based access control
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    """User model with enterprise features"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Info
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Profile Info
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    avatar_url = db.Column(db.String(500))
    
    # Financial
    wallet_balance = db.Column(db.Float, default=1000.00)
    
    # Role & Status
    role = db.Column(db.String(20), default='user')  # user, admin, seller
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # Relationships
    addresses = db.relationship('Address', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    wishlist = db.relationship('WishlistItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Return full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    @property
    def formatted_balance(self):
        """Return formatted wallet balance"""
        return f"${self.wallet_balance:,.2f}"
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def can_afford(self, amount):
        """Check if user can afford a purchase"""
        return self.wallet_balance >= amount
    
    def deduct_balance(self, amount):
        """Deduct from wallet balance"""
        if self.can_afford(amount):
            self.wallet_balance -= amount
            return True
        return False
    
    def add_balance(self, amount):
        """Add to wallet balance"""
        self.wallet_balance += amount
    
    def to_dict(self, include_private=False):
        """Serialize user to dictionary"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'role': self.role,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_private:
            data['wallet_balance'] = self.wallet_balance
            data['formatted_balance'] = self.formatted_balance
            data['phone'] = self.phone
            data['is_active'] = self.is_active
            data['last_login'] = self.last_login.isoformat() if self.last_login else None
        
        return data


class Address(db.Model):
    """User address model"""
    __tablename__ = 'addresses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    address_type = db.Column(db.String(20), default='home')  # home, work, other
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address_line1 = db.Column(db.String(200), nullable=False)
    address_line2 = db.Column(db.String(200))
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), default='India')
    is_default = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'address_type': self.address_type,
            'full_name': self.full_name,
            'phone': self.phone,
            'address_line1': self.address_line1,
            'address_line2': self.address_line2,
            'city': self.city,
            'state': self.state,
            'postal_code': self.postal_code,
            'country': self.country,
            'is_default': self.is_default
        }
