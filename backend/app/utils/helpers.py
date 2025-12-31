"""
FlaskMarket Enterprise - Utility Helpers
Common helper functions
"""

import re
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename


def generate_slug(text):
    """
    Generate URL-friendly slug from text
    """
    # Convert to lowercase
    slug = text.lower()
    # Replace spaces with hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove special characters
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    # Remove multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    
    return slug


def generate_unique_filename(filename):
    """
    Generate unique filename for uploads
    """
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    unique_name = f"{uuid.uuid4().hex}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    return f"{unique_name}.{ext}" if ext else unique_name


def allowed_file(filename, allowed_extensions=None):
    """
    Check if file extension is allowed
    """
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def format_currency(amount, currency='USD', locale='en_US'):
    """
    Format amount as currency
    """
    if currency == 'USD':
        return f"${amount:,.2f}"
    elif currency == 'INR':
        return f"₹{amount:,.2f}"
    return f"{amount:,.2f}"


def truncate_text(text, length=100, suffix='...'):
    """
    Truncate text to specified length
    """
    if len(text) <= length:
        return text
    return text[:length].rsplit(' ', 1)[0] + suffix


def parse_sort_param(sort_string, allowed_fields):
    """
    Parse sort parameter for SQLAlchemy
    Format: "field_asc" or "field_desc"
    Returns: (field_name, direction)
    """
    if not sort_string:
        return None, None
    
    parts = sort_string.rsplit('_', 1)
    if len(parts) != 2:
        return None, None
    
    field, direction = parts
    
    if field not in allowed_fields or direction not in ['asc', 'desc']:
        return None, None
    
    return field, direction


def calculate_pagination(page, per_page, total):
    """
    Calculate pagination metadata
    """
    total_pages = (total + per_page - 1) // per_page
    
    return {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_items': total,
        'has_next': page < total_pages,
        'has_prev': page > 1,
        'next_page': page + 1 if page < total_pages else None,
        'prev_page': page - 1 if page > 1 else None
    }


def validate_email(email):
    """
    Validate email format
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone):
    """
    Validate phone number format
    """
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    # Check if it's a valid phone number (10-15 digits, optionally starting with +)
    pattern = r'^\+?[0-9]{10,15}$'
    return re.match(pattern, cleaned) is not None


def mask_email(email):
    """
    Mask email for privacy
    example@gmail.com -> ex***le@gmail.com
    """
    parts = email.split('@')
    if len(parts) != 2:
        return email
    
    username = parts[0]
    domain = parts[1]
    
    if len(username) <= 2:
        masked = username[0] + '*' * (len(username) - 1)
    else:
        masked = username[:2] + '*' * (len(username) - 4) + username[-2:]
    
    return f"{masked}@{domain}"


def mask_phone(phone):
    """
    Mask phone number for privacy
    1234567890 -> ******7890
    """
    if len(phone) < 4:
        return '*' * len(phone)
    return '*' * (len(phone) - 4) + phone[-4:]
