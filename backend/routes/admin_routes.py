"""
Admin API routes for Threads of Tradition platform.
Handles admin login and artisan verification management.
"""

from flask import Blueprint, request, jsonify
from models import db, Admin, Artisan
from auth import hash_password, verify_password, generate_token, admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/login', methods=['POST'])
def admin_login():
    """Login an admin user."""
    try:
        data = request.get_json()
        
        if not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400
        
        # Find admin
        admin = Admin.query.filter_by(username=data['username']).first()
        if not admin:
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Verify password
        if not verify_password(data['password'], admin.password_hash):
            return jsonify({'error': 'Invalid username or password'}), 401
        
        # Generate token
        token = generate_token(admin.id, 'admin')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'admin': admin.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/artisans', methods=['GET'])
@admin_required
def list_artisans():
    """Get list of all artisans for admin management."""
    try:
        # Get query parameters
        status = request.args.get('status')  # pending, verified, rejected
        
        query = Artisan.query
        
        if status:
            query = query.filter(Artisan.verification_status == status)
        
        artisans = query.order_by(Artisan.created_at.desc()).all()
        
        return jsonify({
            'artisans': [artisan.to_dict() for artisan in artisans],
            'total': len(artisans)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/artisans/<int:artisan_id>', methods=['GET'])
@admin_required
def get_artisan(artisan_id):
    """Get a single artisan's details."""
    try:
        artisan = Artisan.query.get(artisan_id)
        if not artisan:
            return jsonify({'error': 'Artisan not found'}), 404
        
        return jsonify({'artisan': artisan.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/artisans/<int:artisan_id>/verify', methods=['POST'])
@admin_required
def verify_artisan(artisan_id):
    """Verify or reject an artisan."""
    try:
        artisan = Artisan.query.get(artisan_id)
        if not artisan:
            return jsonify({'error': 'Artisan not found'}), 404
        
        data = request.get_json()
        action = data.get('action', 'verify')  # verify or reject
        
        if action == 'verify':
            artisan.is_verified = True
            artisan.verification_status = 'verified'
            message = f'Artisan {artisan.name} has been verified'
        elif action == 'reject':
            artisan.is_verified = False
            artisan.verification_status = 'rejected'
            message = f'Artisan {artisan.name} has been rejected'
        else:
            return jsonify({'error': 'Invalid action. Use "verify" or "reject"'}), 400
        
        db.session.commit()
        
        return jsonify({
            'message': message,
            'artisan': artisan.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    """Get dashboard statistics."""
    try:
        total_artisans = Artisan.query.count()
        verified_artisans = Artisan.query.filter_by(is_verified=True).count()
        pending_artisans = Artisan.query.filter_by(verification_status='pending').count()
        
        from models import Product
        total_products = Product.query.count()
        
        return jsonify({
            'stats': {
                'total_artisans': total_artisans,
                'verified_artisans': verified_artisans,
                'pending_artisans': pending_artisans,
                'total_products': total_products
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def create_default_admin():
    """Create a default admin user if none exists."""
    from flask import current_app
    with current_app.app_context():
        if Admin.query.count() == 0:
            admin = Admin(
                username='admin',
                password_hash=hash_password('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            print("Default admin created: username='admin', password='admin123'")
