"""
Product API routes for Threads of Tradition platform.
Handles product upload, listing, and AI feature generation.
"""

from flask import Blueprint, request, jsonify, current_app
from models import db, Product, Artisan
from auth import artisan_required
from ai_services import generate_caption, recommend_price, get_available_materials
import os
import uuid

product_bp = Blueprint('product', __name__, url_prefix='/api/products')

# Upload folder for product images
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'products')


@product_bp.route('/materials', methods=['GET'])
def get_materials():
    """Get list of available materials for dropdown."""
    return jsonify({'materials': get_available_materials()}), 200


@product_bp.route('/generate-caption', methods=['POST'])
@artisan_required
def api_generate_caption():
    """Generate AI caption for a product (preview before upload)."""
    try:
        data = request.get_json()
        
        required_fields = ['material', 'time_spent']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Get artisan info
        artisan = Artisan.query.get(request.user_id)
        if not artisan:
            return jsonify({'error': 'Artisan not found'}), 404
        
        caption = generate_caption(
            material=data['material'],
            time_spent=float(data['time_spent']),
            artisan_name=artisan.name,
            location=artisan.location
        )
        
        return jsonify({'caption': caption}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('/recommend-price', methods=['POST'])
@artisan_required
def api_recommend_price():
    """Get AI price recommendation for a product."""
    try:
        data = request.get_json()
        
        required_fields = ['material', 'time_spent']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        min_price, max_price = recommend_price(
            material=data['material'],
            time_spent=float(data['time_spent'])
        )
        
        return jsonify({
            'price_min': min_price,
            'price_max': max_price,
            'price_display': f"₹{min_price:,.0f} - ₹{max_price:,.0f}"
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('/upload', methods=['POST'])
@artisan_required
def upload_product():
    """Upload a new product with image."""
    try:
        # Get artisan
        artisan = Artisan.query.get(request.user_id)
        if not artisan:
            return jsonify({'error': 'Artisan not found'}), 404
        
        # Validate required fields
        material = request.form.get('material')
        time_spent = request.form.get('time_spent')
        
        if not material or not time_spent:
            return jsonify({'error': 'Material and time_spent are required'}), 400
        
        # Handle image upload
        if 'image' not in request.files:
            return jsonify({'error': 'Product image is required'}), 400
        
        image_file = request.files['image']
        if not image_file.filename:
            return jsonify({'error': 'No image selected'}), 400
        
        # Save image
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Generate unique filename
        file_ext = os.path.splitext(image_file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_ext}"
        image_path = os.path.join('products', unique_filename)
        image_file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
        
        # Generate AI content
        caption = request.form.get('caption')
        if not caption:
            caption = generate_caption(
                material=material,
                time_spent=float(time_spent),
                artisan_name=artisan.name,
                location=artisan.location
            )
        
        # Get price recommendation
        price_min = request.form.get('price_min')
        price_max = request.form.get('price_max')
        
        if not price_min or not price_max:
            price_min, price_max = recommend_price(
                material=material,
                time_spent=float(time_spent)
            )
        else:
            price_min = float(price_min)
            price_max = float(price_max)
        
        # Generate certificate ID
        certificate_id = f"TOT-{uuid.uuid4().hex[:8].upper()}"
        
        # Create product
        product = Product(
            artisan_id=artisan.id,
            image_path=image_path,
            material=material,
            time_spent=float(time_spent),
            caption=caption,
            price_min=price_min,
            price_max=price_max,
            certificate_id=certificate_id
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product uploaded successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@product_bp.route('/', methods=['GET'])
def list_products():
    """List all products for shopping portal."""
    try:
        # Get query parameters for filtering
        material = request.args.get('material')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        verified_only = request.args.get('verified_only', 'false').lower() == 'true'
        
        # Base query
        query = Product.query.join(Artisan)
        
        # Apply filters
        if material:
            query = query.filter(Product.material == material)
        
        if min_price is not None:
            query = query.filter(Product.price_min >= min_price)
        
        if max_price is not None:
            query = query.filter(Product.price_max <= max_price)
        
        if verified_only:
            query = query.filter(Artisan.is_verified == True)
        
        # Order by newest first
        products = query.order_by(Product.created_at.desc()).all()
        
        return jsonify({
            'products': [product.to_dict() for product in products],
            'total': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@product_bp.route('/<int:product_id>', methods=['DELETE'])
@artisan_required
def delete_product(product_id):
    """Delete a product (only by owner)."""
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check ownership
        if product.artisan_id != request.user_id:
            return jsonify({'error': 'You can only delete your own products'}), 403
        
        # Delete image file
        image_full_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'uploads',
            product.image_path
        )
        if os.path.exists(image_full_path):
            os.remove(image_full_path)
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
