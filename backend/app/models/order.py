"""
FlaskMarket Enterprise - Order & Cart Models
Complete order management with cart, checkout, and transaction tracking
"""

from datetime import datetime
from app.extensions import db
import uuid


class CartItem(db.Model):
    """Shopping cart item"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    quantity = db.Column(db.Integer, default=1)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = db.relationship('Product')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'product_id', name='unique_cart_item'),
    )
    
    @property
    def subtotal(self):
        """Calculate item subtotal"""
        return self.product.price * self.quantity
    
    def to_dict(self):
        return {
            'id': self.id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity,
            'subtotal': self.subtotal,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Order Status
    status = db.Column(db.String(30), default='pending')
    # pending, confirmed, processing, shipped, delivered, cancelled, refunded
    
    # Pricing
    subtotal = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0)
    shipping_cost = db.Column(db.Float, default=0)
    tax_amount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Payment
    payment_method = db.Column(db.String(50), default='wallet')
    payment_status = db.Column(db.String(30), default='pending')
    # pending, paid, failed, refunded
    
    # Shipping Address (stored as JSON for order history)
    shipping_address = db.Column(db.JSON)
    
    # Notes
    customer_notes = db.Column(db.Text)
    admin_notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shipped_at = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic',
                           cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='order', lazy='dynamic')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    @staticmethod
    def generate_order_number():
        """Generate unique order number"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().hex)[:6].upper()
        return f'ORD-{timestamp}-{unique_id}'
    
    def calculate_totals(self):
        """Calculate order totals from items"""
        self.subtotal = sum(item.subtotal for item in self.items)
        self.total_amount = self.subtotal - self.discount_amount + self.shipping_cost + self.tax_amount
    
    def to_dict(self, include_items=False):
        data = {
            'id': self.id,
            'order_number': self.order_number,
            'status': self.status,
            'subtotal': self.subtotal,
            'discount_amount': self.discount_amount,
            'shipping_cost': self.shipping_cost,
            'tax_amount': self.tax_amount,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'shipping_address': self.shipping_address,
            'item_count': self.items.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'shipped_at': self.shipped_at.isoformat() if self.shipped_at else None,
            'delivered_at': self.delivered_at.isoformat() if self.delivered_at else None
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
        
        return data


class OrderItem(db.Model):
    """Order line item"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    # Store product details at time of purchase
    product_name = db.Column(db.String(200), nullable=False)
    product_sku = db.Column(db.String(50))
    product_image = db.Column(db.String(500))
    
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0)
    
    product = db.relationship('Product')
    
    @property
    def subtotal(self):
        """Calculate line item subtotal"""
        return (self.unit_price * self.quantity) - self.discount
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'product_sku': self.product_sku,
            'product_image': self.product_image,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'discount': self.discount,
            'subtotal': self.subtotal
        }


class Transaction(db.Model):
    """Financial transaction log"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    
    # Transaction Type
    transaction_type = db.Column(db.String(30), nullable=False)
    # purchase, refund, wallet_credit, wallet_debit
    
    amount = db.Column(db.Float, nullable=False)
    balance_before = db.Column(db.Float)
    balance_after = db.Column(db.Float)
    
    status = db.Column(db.String(30), default='completed')
    # pending, completed, failed
    
    description = db.Column(db.String(500))
    transaction_data = db.Column(db.JSON)  # Additional transaction data
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='transactions')
    
    @staticmethod
    def generate_transaction_id():
        """Generate unique transaction ID"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        unique_id = str(uuid.uuid4().hex)[:8].upper()
        return f'TXN-{timestamp}-{unique_id}'
    
    def to_dict(self):
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'transaction_type': self.transaction_type,
            'amount': self.amount,
            'balance_before': self.balance_before,
            'balance_after': self.balance_after,
            'status': self.status,
            'description': self.description,
            'order_number': self.order.order_number if self.order else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Coupon(db.Model):
    """Discount coupon model"""
    __tablename__ = 'coupons'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    discount_type = db.Column(db.String(20), nullable=False)  # percentage, fixed
    discount_value = db.Column(db.Float, nullable=False)
    
    min_order_amount = db.Column(db.Float, default=0)
    max_discount_amount = db.Column(db.Float)  # Cap for percentage discounts
    
    usage_limit = db.Column(db.Integer)  # Total usage limit
    used_count = db.Column(db.Integer, default=0)
    per_user_limit = db.Column(db.Integer, default=1)
    
    is_active = db.Column(db.Boolean, default=True)
    starts_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_valid(self):
        """Check if coupon is valid"""
        now = datetime.utcnow()
        
        if not self.is_active:
            return False, "Coupon is inactive"
        
        if self.starts_at and now < self.starts_at:
            return False, "Coupon not yet active"
        
        if self.expires_at and now > self.expires_at:
            return False, "Coupon has expired"
        
        if self.usage_limit and self.used_count >= self.usage_limit:
            return False, "Coupon usage limit reached"
        
        return True, "Valid"
    
    def calculate_discount(self, order_total):
        """Calculate discount for an order"""
        if order_total < self.min_order_amount:
            return 0
        
        if self.discount_type == 'percentage':
            discount = order_total * (self.discount_value / 100)
            if self.max_discount_amount:
                discount = min(discount, self.max_discount_amount)
        else:
            discount = self.discount_value
        
        return min(discount, order_total)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'min_order_amount': self.min_order_amount,
            'max_discount_amount': self.max_discount_amount,
            'is_active': self.is_active,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None
        }

