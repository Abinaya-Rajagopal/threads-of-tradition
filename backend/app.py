"""
Threads of Tradition - Main Flask Application
A platform connecting Indian handloom artisans with customers.
"""

import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from models import db, Admin
from auth import hash_password

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'threads-of-tradition-secret-key-2024'

# Create database directory with absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, '..', 'database')
os.makedirs(DB_DIR, exist_ok=True)
DB_PATH = os.path.join(DB_DIR, 'threads.db')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Enable CORS for frontend
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize database
db.init_app(app)

# Create upload directories
UPLOAD_BASE = os.path.join(BASE_DIR, 'uploads')
os.makedirs(os.path.join(UPLOAD_BASE, 'products'), exist_ok=True)
os.makedirs(os.path.join(UPLOAD_BASE, 'certificates'), exist_ok=True)

# Register blueprints
from routes.artisan_routes import artisan_bp
from routes.product_routes import product_bp
from routes.admin_routes import admin_bp

app.register_blueprint(artisan_bp)
app.register_blueprint(product_bp)
app.register_blueprint(admin_bp)


# Serve uploaded files
@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded files (images, certificates)."""
    return send_from_directory(UPLOAD_BASE, filename)


# Health check endpoint
@app.route('/api/health')
def health_check():
    """API health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Threads of Tradition API is running'
    }), 200


# Root endpoint
@app.route('/api')
def api_info():
    """API information endpoint."""
    return jsonify({
        'name': 'Threads of Tradition API',
        'version': '1.0.0',
        'description': 'Platform connecting Indian handloom artisans with customers',
        'endpoints': {
            'artisan': '/api/artisan',
            'products': '/api/products',
            'admin': '/api/admin',
            'health': '/api/health'
        }
    }), 200


def create_default_admin():
    """Create a default admin user if none exists."""
    if Admin.query.count() == 0:
        admin = Admin(
            username='admin',
            password_hash=hash_password('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Default admin created: username='admin', password='admin123'")


def create_demo_data():
    """Create demo artisans and products for showcasing."""
    from models import Artisan, Product
    from ai_services import generate_caption, recommend_price
    import uuid
    
    # Check if demo data already exists
    if Artisan.query.count() > 0:
        return
    
    print("Creating demo data...")
    
    # Demo artisans
    demo_artisans = [
        {
            'name': 'Lakshmi Devi',
            'location': 'Varanasi, Uttar Pradesh',
            'email': 'lakshmi@demo.com',
            'password': 'demo123',
            'is_verified': True
        },
        {
            'name': 'Ramesh Patwa',
            'location': 'Jaipur, Rajasthan',
            'email': 'ramesh@demo.com',
            'password': 'demo123',
            'is_verified': True
        },
        {
            'name': 'Meena Kumari',
            'location': 'Kanchipuram, Tamil Nadu',
            'email': 'meena@demo.com',
            'password': 'demo123',
            'is_verified': False
        }
    ]
    
    created_artisans = []
    for artisan_data in demo_artisans:
        artisan = Artisan(
            name=artisan_data['name'],
            location=artisan_data['location'],
            email=artisan_data['email'],
            password_hash=hash_password(artisan_data['password']),
            is_verified=artisan_data['is_verified'],
            verification_status='verified' if artisan_data['is_verified'] else 'pending'
        )
        db.session.add(artisan)
        created_artisans.append(artisan)
    
    db.session.commit()
    
    # Demo products
    demo_products = [
        {'artisan_idx': 0, 'material': 'silk', 'time_spent': 48},
        {'artisan_idx': 0, 'material': 'brocade', 'time_spent': 72},
        {'artisan_idx': 1, 'material': 'cotton', 'time_spent': 24},
        {'artisan_idx': 1, 'material': 'wool', 'time_spent': 36},
        {'artisan_idx': 2, 'material': 'silk', 'time_spent': 60},
    ]
    
    for product_data in demo_products:
        artisan = created_artisans[product_data['artisan_idx']]
        material = product_data['material']
        time_spent = product_data['time_spent']
        
        caption = generate_caption(material, time_spent, artisan.name, artisan.location)
        min_price, max_price = recommend_price(material, time_spent)
        
        product = Product(
            artisan_id=artisan.id,
            image_path='products/demo_placeholder.jpg',  # Will be replaced with actual images
            material=material,
            time_spent=time_spent,
            caption=caption,
            price_min=min_price,
            price_max=max_price,
            certificate_id=f"TOT-{uuid.uuid4().hex[:8].upper()}"
        )
        db.session.add(product)
    
    db.session.commit()
    print(f"✓ Created {len(demo_artisans)} demo artisans and {len(demo_products)} demo products")


# Initialize database and create tables
with app.app_context():
    db.create_all()
    create_default_admin()
    create_demo_data()
    print("✓ Database initialized successfully")


if __name__ == '__main__':
    print("\n" + "="*50)
    print("🧵 Threads of Tradition API Server")
    print("="*50)
    print("Starting server at http://localhost:5000")
    print("API endpoints available at http://localhost:5000/api")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
