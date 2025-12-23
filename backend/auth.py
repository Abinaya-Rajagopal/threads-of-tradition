"""
Authentication utilities for Threads of Tradition platform.
Provides password hashing, JWT token management, and decorators.
"""

import bcrypt
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


def generate_token(user_id: int, user_type: str = 'artisan', expires_hours: int = 24) -> str:
    """
    Generate a JWT token for authentication.
    
    Args:
        user_id: ID of the user
        user_type: Type of user ('artisan' or 'admin')
        expires_hours: Token expiration time in hours
    
    Returns:
        JWT token string
    """
    payload = {
        'user_id': user_id,
        'user_type': user_type,
        'exp': datetime.utcnow() + timedelta(hours=expires_hours),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_token(token: str) -> dict:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded token payload
    
    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid
    """
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])


def login_required(f):
    """Decorator to require authentication for a route."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid authorization header format'}), 401
        
        if not token:
            return jsonify({'error': 'Authentication token is missing'}), 401
        
        try:
            payload = decode_token(token)
            request.user_id = payload['user_id']
            request.user_type = payload['user_type']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function


def artisan_required(f):
    """Decorator to require artisan authentication."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if request.user_type != 'artisan':
            return jsonify({'error': 'Artisan access required'}), 403
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """Decorator to require admin authentication."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if request.user_type != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    
    return decorated_function
