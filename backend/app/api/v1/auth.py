"""
FlaskMarket Enterprise - Authentication API
JWT-based authentication with register, login, logout, refresh
"""

from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity, current_user,
    get_jwt
)
from datetime import datetime
from app.api.v1 import api_v1_bp
from app.extensions import db, limiter
from app.models import User


# Token blacklist (in production, use Redis)
token_blacklist = set()


@api_v1_bp.route('/auth/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """
    Register a new user
    ---
    Request Body:
        - username: string (required)
        - email: string (required)
        - password: string (required)
        - first_name: string (optional)
        - last_name: string (optional)
    """
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'success': False,
                'message': f'{field} is required'
            }), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            'success': False,
            'message': 'Username already exists'
        }), 409
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({
            'success': False,
            'message': 'Email already registered'
        }), 409
    
    # Validate password strength
    if len(data['password']) < 6:
        return jsonify({
            'success': False,
            'message': 'Password must be at least 6 characters'
        }), 400
    
    # Create user
    user = User(
        username=data['username'],
        email=data['email'].lower(),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        wallet_balance=1000.00  # Starting balance
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Generate tokens
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'data': {
                'user': user.to_dict(include_private=True),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Registration failed',
            'error': str(e)
        }), 500


@api_v1_bp.route('/auth/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """
    Login user and return tokens
    ---
    Request Body:
        - username: string (username or email)
        - password: string
    """
    data = request.get_json()
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({
            'success': False,
            'message': 'Username and password are required'
        }), 400
    
    # Find user by username or email
    user = User.query.filter(
        (User.username == username) | (User.email == username.lower())
    ).first()
    
    if not user or not user.check_password(password):
        return jsonify({
            'success': False,
            'message': 'Invalid username or password'
        }), 401
    
    if not user.is_active:
        return jsonify({
            'success': False,
            'message': 'Your account has been deactivated'
        }), 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Generate tokens
    access_token = create_access_token(identity=user)
    refresh_token = create_refresh_token(identity=user)
    
    return jsonify({
        'success': True,
        'message': 'Login successful',
        'data': {
            'user': user.to_dict(include_private=True),
            'access_token': access_token,
            'refresh_token': refresh_token
        }
    })


@api_v1_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh access token using refresh token
    """
    identity = get_jwt_identity()
    user = User.query.get(identity)
    
    if not user:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404
    
    access_token = create_access_token(identity=user)
    
    return jsonify({
        'success': True,
        'data': {
            'access_token': access_token
        }
    })


@api_v1_bp.route('/auth/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    Logout user (invalidate token)
    """
    jti = get_jwt()['jti']
    token_blacklist.add(jti)
    
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })


@api_v1_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user
    """
    return jsonify({
        'success': True,
        'data': {
            'user': current_user.to_dict(include_private=True)
        }
    })


@api_v1_bp.route('/auth/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """
    Update current user profile
    """
    data = request.get_json()
    user = current_user
    
    # Update allowed fields
    allowed_fields = ['first_name', 'last_name', 'phone', 'avatar_url']
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    # Update password if provided
    if data.get('new_password'):
        if not data.get('current_password'):
            return jsonify({
                'success': False,
                'message': 'Current password is required'
            }), 400
        
        if not user.check_password(data['current_password']):
            return jsonify({
                'success': False,
                'message': 'Current password is incorrect'
            }), 400
        
        user.set_password(data['new_password'])
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'data': {
                'user': user.to_dict(include_private=True)
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': 'Update failed',
            'error': str(e)
        }), 500


@api_v1_bp.route('/auth/check-token', methods=['GET'])
@jwt_required()
def check_token():
    """
    Verify if token is valid
    """
    return jsonify({
        'success': True,
        'message': 'Token is valid',
        'data': {
            'user_id': current_user.id,
            'username': current_user.username
        }
    })
