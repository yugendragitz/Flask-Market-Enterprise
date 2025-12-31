"""
FlaskMarket Enterprise - Application Entry Point
Run this file to start the development server
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app import create_app
from app.extensions import db

# Create application instance
app = create_app(os.getenv('FLASK_ENV', 'development'))


@app.cli.command('init-db')
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        print('✅ Database initialized successfully!')


@app.cli.command('seed-db')
def seed_db():
    """Seed the database with sample data."""
    from seed import seed_database
    with app.app_context():
        seed_database()
        print('✅ Database seeded successfully!')


@app.cli.command('reset-db')
def reset_db():
    """Reset and reseed the database."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        from seed import seed_database
        seed_database()
        print('✅ Database reset and seeded successfully!')


@app.shell_context_processor
def make_shell_context():
    """Add models to shell context for easy debugging."""
    from app.models.user import User, Address
    from app.models.product import Product, Category, Review, WishlistItem
    from app.models.order import CartItem, Order, OrderItem, Transaction, Coupon
    
    return {
        'db': db,
        'User': User,
        'Address': Address,
        'Product': Product,
        'Category': Category,
        'Review': Review,
        'WishlistItem': WishlistItem,
        'CartItem': CartItem,
        'Order': Order,
        'OrderItem': OrderItem,
        'Transaction': Transaction,
        'Coupon': Coupon
    }


if __name__ == '__main__':
    # Run development server
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=os.getenv('FLASK_ENV') == 'development'
    )
