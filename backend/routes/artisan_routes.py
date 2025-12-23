"""
Artisan API routes for Threads of Tradition platform.
Handles artisan registration, login, and profile management.
"""

from flask import Blueprint, request, jsonify
from models import db, Artisan
from auth import hash_password, verify_password, generate_token, artisan_required
import os

artisan_bp = Blueprint('artisan', __name__, url_prefix='/api/artisan')

# Upload folder for certificates
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'certificates')


@artisan_bp.route('/register', methods=['POST'])
def register():
    """Register a new artisan."""
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Validate required fields
        required_fields = ['name', 'location', 'email', 'password']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if email already exists
        existing_artisan = Artisan.query.filter_by(email=data['email']).first()
        if existing_artisan:
            return jsonify({'error': 'Email already registered'}), 409
        
        # Handle certificate upload
        certificate_path = None
        if 'certificate' in request.files:
            file = request.files['certificate']
            if file.filename:
                # Ensure upload directory exists
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Save file with unique name
                filename = f"{data['email'].replace('@', '_').replace('.', '_')}_{file.filename}"
                certificate_path = os.path.join('certificates', filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
        
        # Create new artisan
        artisan = Artisan(
            name=data['name'],
            location=data['location'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            certificate_path=certificate_path,
            is_verified=False,
            verification_status='pending'
        )
        
        db.session.add(artisan)
        db.session.commit()
        
        # Generate token
        token = generate_token(artisan.id, 'artisan')
        
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'artisan': artisan.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@artisan_bp.route('/login', methods=['POST'])
def login():
    """Login an artisan."""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Find artisan
        artisan = Artisan.query.filter_by(email=data['email']).first()
        if not artisan:
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Verify password
        if not verify_password(data['password'], artisan.password_hash):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        # Generate token
        token = generate_token(artisan.id, 'artisan')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'artisan': artisan.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@artisan_bp.route('/profile', methods=['GET'])
@artisan_required
def get_profile():
    """Get current artisan's profile."""
    try:
        artisan = Artisan.query.get(request.user_id)
        if not artisan:
            return jsonify({'error': 'Artisan not found'}), 404
        
        return jsonify({'artisan': artisan.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@artisan_bp.route('/profile', methods=['PUT'])
@artisan_required
def update_profile():
    """Update current artisan's profile."""
    try:
        artisan = Artisan.query.get(request.user_id)
        if not artisan:
            return jsonify({'error': 'Artisan not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if data.get('name'):
            artisan.name = data['name']
        if data.get('location'):
            artisan.location = data['location']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'artisan': artisan.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@artisan_bp.route('/products', methods=['GET'])
@artisan_required
def get_my_products():
    """Get products uploaded by the current artisan."""
    try:
        artisan = Artisan.query.get(request.user_id)
        if not artisan:
            return jsonify({'error': 'Artisan not found'}), 404
        
        products = [product.to_dict() for product in artisan.products]
        
        return jsonify({'products': products}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
