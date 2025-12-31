"""
FlaskMarket Enterprise - API v1 Blueprint
Main API blueprint registration
"""

from flask import Blueprint

api_v1_bp = Blueprint('api_v1', __name__)

# Import routes after blueprint creation to avoid circular imports
from app.api.v1 import auth
from app.api.v1 import products
from app.api.v1 import cart
from app.api.v1 import orders
from app.api.v1 import users
from app.api.v1 import admin
