"""
FlaskMarket Enterprise - Utility Decorators
Custom decorators for authorization and validation
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import current_user


def admin_required(f):
    """
    Decorator to require admin role
    Use after @jwt_required()
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user or not current_user.is_admin():
            return jsonify({
                'success': False,
                'error': 'Admin Access Required',
                'message': 'You do not have permission to access this resource'
            }), 403
        return f(*args, **kwargs)
    return decorated_function


def seller_required(f):
    """
    Decorator to require seller or admin role
    Use after @jwt_required()
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user or current_user.role not in ['admin', 'seller']:
            return jsonify({
                'success': False,
                'error': 'Seller Access Required',
                'message': 'You do not have permission to access this resource'
            }), 403
        return f(*args, **kwargs)
    return decorated_function


def verified_required(f):
    """
    Decorator to require verified email
    Use after @jwt_required()
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user or not current_user.is_verified:
            return jsonify({
                'success': False,
                'error': 'Email Verification Required',
                'message': 'Please verify your email to access this feature'
            }), 403
        return f(*args, **kwargs)
    return decorated_function


def rate_limit_by_user(limit_string):
    """
    Rate limit by user ID instead of IP
    Usage: @rate_limit_by_user("5 per minute")
    """
    from flask_limiter import Limiter
    from flask_jwt_extended import get_jwt_identity
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # This is a placeholder - actual implementation would use
            # custom key_func in limiter
            return f(*args, **kwargs)
        return decorated_function
    return decorator
