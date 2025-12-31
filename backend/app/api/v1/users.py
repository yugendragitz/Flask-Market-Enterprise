"""
FlaskMarket Enterprise - Users API
User profile and address management
"""

from flask import request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app.api.v1 import api_v1_bp
from app.extensions import db
from app.models import User, Address


@api_v1_bp.route('/users/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """
    Get current user's profile
    """
    return jsonify({
        'success': True,
        'data': {
            'user': current_user.to_dict(include_private=True)
        }
    })


@api_v1_bp.route('/users/wallet', methods=['GET'])
@jwt_required()
def get_wallet():
    """
    Get wallet balance and recent transactions
    """
    from app.models import Transaction
    from sqlalchemy import desc
    
    recent_transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(desc(Transaction.created_at)).limit(5).all()
    
    return jsonify({
        'success': True,
        'data': {
            'balance': current_user.wallet_balance,
            'formatted_balance': current_user.formatted_balance,
            'recent_transactions': [t.to_dict() for t in recent_transactions]
        }
    })


@api_v1_bp.route('/users/wallet/add', methods=['POST'])
@jwt_required()
def add_wallet_funds():
    """
    Add funds to wallet (simulated)
    """
    from app.models import Transaction
    
    data = request.get_json()
    amount = data.get('amount')
    
    if not amount or amount <= 0:
        return jsonify({
            'success': False,
            'message': 'Valid amount is required'
        }), 400
    
    if amount > 10000:
        return jsonify({
            'success': False,
            'message': 'Maximum add limit is $10,000'
        }), 400
    
    balance_before = current_user.wallet_balance
    current_user.add_balance(amount)
    
    # Create transaction record
    transaction = Transaction(
        transaction_id=Transaction.generate_transaction_id(),
        user_id=current_user.id,
        transaction_type='wallet_credit',
        amount=amount,
        balance_before=balance_before,
        balance_after=current_user.wallet_balance,
        status='completed',
        description=f'Wallet top-up: ${amount:.2f}'
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'${amount:.2f} added to wallet',
        'data': {
            'balance': current_user.wallet_balance,
            'formatted_balance': current_user.formatted_balance
        }
    })


# ============ Addresses ============

@api_v1_bp.route('/users/addresses', methods=['GET'])
@jwt_required()
def get_addresses():
    """
    Get all user addresses
    """
    addresses = current_user.addresses.all()
    
    return jsonify({
        'success': True,
        'data': {
            'addresses': [addr.to_dict() for addr in addresses]
        }
    })


@api_v1_bp.route('/users/addresses', methods=['POST'])
@jwt_required()
def add_address():
    """
    Add a new address
    """
    data = request.get_json()
    
    required_fields = ['full_name', 'phone', 'address_line1', 'city', 'state', 'postal_code']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'success': False,
                'message': f'{field} is required'
            }), 400
    
    # If this is the first address or marked as default, set as default
    is_default = data.get('is_default', False)
    if is_default or current_user.addresses.count() == 0:
        # Remove default from other addresses
        Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
        is_default = True
    
    address = Address(
        user_id=current_user.id,
        address_type=data.get('address_type', 'home'),
        full_name=data['full_name'],
        phone=data['phone'],
        address_line1=data['address_line1'],
        address_line2=data.get('address_line2'),
        city=data['city'],
        state=data['state'],
        postal_code=data['postal_code'],
        country=data.get('country', 'India'),
        is_default=is_default
    )
    
    db.session.add(address)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Address added successfully',
        'data': {
            'address': address.to_dict()
        }
    }), 201


@api_v1_bp.route('/users/addresses/<int:address_id>', methods=['PUT'])
@jwt_required()
def update_address(address_id):
    """
    Update an address
    """
    address = Address.query.filter_by(
        id=address_id, user_id=current_user.id
    ).first_or_404()
    
    data = request.get_json()
    
    # Update fields
    allowed_fields = ['address_type', 'full_name', 'phone', 'address_line1', 
                      'address_line2', 'city', 'state', 'postal_code', 'country']
    for field in allowed_fields:
        if field in data:
            setattr(address, field, data[field])
    
    # Handle default address
    if data.get('is_default'):
        Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
        address.is_default = True
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Address updated successfully',
        'data': {
            'address': address.to_dict()
        }
    })


@api_v1_bp.route('/users/addresses/<int:address_id>', methods=['DELETE'])
@jwt_required()
def delete_address(address_id):
    """
    Delete an address
    """
    address = Address.query.filter_by(
        id=address_id, user_id=current_user.id
    ).first_or_404()
    
    was_default = address.is_default
    
    db.session.delete(address)
    
    # If deleted address was default, make another one default
    if was_default:
        other_address = Address.query.filter_by(user_id=current_user.id).first()
        if other_address:
            other_address.is_default = True
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Address deleted successfully'
    })


@api_v1_bp.route('/users/addresses/<int:address_id>/default', methods=['PUT'])
@jwt_required()
def set_default_address(address_id):
    """
    Set address as default
    """
    address = Address.query.filter_by(
        id=address_id, user_id=current_user.id
    ).first_or_404()
    
    # Remove default from all addresses
    Address.query.filter_by(user_id=current_user.id, is_default=True).update({'is_default': False})
    
    address.is_default = True
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Default address updated'
    })
