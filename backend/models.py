"""
Database models for Threads of Tradition platform.
Defines Artisan and Product tables with SQLAlchemy ORM.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


class Artisan(db.Model):
    """Model representing an artisan who creates handmade products."""
    
    __tablename__ = 'artisans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    certificate_path = db.Column(db.String(255), nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    verification_status = db.Column(db.String(50), default='pending')  # pending, verified, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with products
    products = db.relationship('Product', backref='artisan', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert artisan to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'email': self.email,
            'is_verified': self.is_verified,
            'verification_status': self.verification_status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'product_count': len(self.products)
        }


class Product(db.Model):
    """Model representing a handmade product created by an artisan."""
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    artisan_id = db.Column(db.Integer, db.ForeignKey('artisans.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    material = db.Column(db.String(50), nullable=False)
    time_spent = db.Column(db.Float, nullable=False)  # in hours
    caption = db.Column(db.Text, nullable=False)
    price_min = db.Column(db.Float, nullable=False)
    price_max = db.Column(db.Float, nullable=False)
    certificate_id = db.Column(db.String(50), nullable=False)  # Fake certificate ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)
        # Auto-generate fake certificate ID if not provided
        if not self.certificate_id:
            self.certificate_id = f"TOT-{uuid.uuid4().hex[:8].upper()}"
    
    def to_dict(self):
        """Convert product to dictionary for API responses."""
        return {
            'id': self.id,
            'artisan_id': self.artisan_id,
            'artisan_name': self.artisan.name if self.artisan else None,
            'artisan_location': self.artisan.location if self.artisan else None,
            'artisan_verified': self.artisan.is_verified if self.artisan else False,
            'image_path': self.image_path,
            'material': self.material,
            'time_spent': self.time_spent,
            'caption': self.caption,
            'price_min': self.price_min,
            'price_max': self.price_max,
            'certificate_id': self.certificate_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Admin(db.Model):
    """Model representing an admin user."""
    
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
