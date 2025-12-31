"""
FlaskMarket Enterprise - Flask Extensions
Centralized extension initialization
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Database ORM
db = SQLAlchemy()

# Database migrations
migrate = Migrate()

# JWT Authentication
jwt = JWTManager()

# Serialization/Deserialization
ma = Marshmallow()

# Rate limiting
limiter = Limiter(key_func=get_remote_address)


# JWT Callbacks for enhanced functionality
@jwt.user_identity_loader
def user_identity_lookup(user):
    """Return user id as identity"""
    return user.id if hasattr(user, 'id') else user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """Load user from database on each request"""
    from app.models.user import User
    identity = jwt_data["sub"]
    return User.query.get(identity)


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired tokens"""
    return {
        'success': False,
        'error': 'Token Expired',
        'message': 'Your session has expired. Please log in again.'
    }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid tokens"""
    return {
        'success': False,
        'error': 'Invalid Token',
        'message': 'Token verification failed.'
    }, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing tokens"""
    return {
        'success': False,
        'error': 'Authorization Required',
        'message': 'Please provide a valid access token.'
    }, 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """Handle revoked tokens"""
    return {
        'success': False,
        'error': 'Token Revoked',
        'message': 'This token has been revoked.'
    }, 401
