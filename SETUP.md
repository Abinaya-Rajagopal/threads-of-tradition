# Threads of Tradition - Setup Guide

A full-stack platform connecting Indian handloom artisans with customers, featuring AI-powered caption generation and price recommendations.

## Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- A modern web browser (Chrome, Firefox, Edge, Safari)

## Project Structure

```
threads-of-tradition/
├── backend/                 # Flask API server
│   ├── app.py              # Main application
│   ├── models.py           # Database models
│   ├── ai_services.py      # AI caption & price logic
│   ├── auth.py             # Authentication utilities
│   ├── routes/             # API route handlers
│   └── requirements.txt    # Python dependencies
├── frontend/               # Static HTML/CSS/JS frontend
│   ├── index.html          # Main landing page
│   ├── artisan/            # Artisan portal pages
│   ├── shop/               # Shopping portal
│   ├── admin/              # Admin dashboard
│   ├── css/                # Stylesheets
│   └── js/                 # JavaScript helpers
├── database/               # SQLite database (auto-created)
├── README.md               # Project requirements
└── SETUP.md               # This file
```

## Quick Start

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Backend Server

```bash
cd backend
python app.py
```

The server will start at `http://localhost:5000`

You should see:
```
==================================================
🧵 Threads of Tradition API Server
==================================================
Starting server at http://localhost:5000
API endpoints available at http://localhost:5000/api
==================================================
```

### 3. Open the Frontend

Open the frontend in your browser. You can either:

**Option A**: Open the file directly
- Navigate to `frontend/index.html` and open it in your browser

**Option B**: Use a simple HTTP server (recommended)
```bash
cd frontend
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser

## Demo Accounts

The system comes with pre-created demo accounts:

### Artisan Accounts
| Email | Password | Status |
|-------|----------|--------|
| lakshmi@demo.com | demo123 | Verified |
| ramesh@demo.com | demo123 | Verified |
| meena@demo.com | demo123 | Pending |

### Admin Account
| Username | Password |
|----------|----------|
| admin | admin123 |

## Features Walkthrough

### 1. Artisan Portal (`/frontend/artisan/`)
- **Register**: Create a new artisan account
- **Login**: Access your dashboard
- **Dashboard**: View profile and products
- **Upload**: Add new products with AI-generated captions and prices

### 2. Shopping Portal (`/frontend/shop/`)
- Browse all products from artisans
- Filter by material, price, and verification status
- View product details with artisan information
- See verified badges on trusted artisan products

### 3. Admin Panel (`/frontend/admin/`)
- Login with admin credentials
- View platform statistics
- Verify or reject artisan registrations
- Filter artisans by status

## API Endpoints

### Health Check
- `GET /api/health` - Check if API is running

### Artisan Routes
- `POST /api/artisan/register` - Register new artisan
- `POST /api/artisan/login` - Login
- `GET /api/artisan/profile` - Get profile (auth required)
- `GET /api/artisan/products` - Get own products (auth required)

### Product Routes
- `GET /api/products/` - List all products
- `GET /api/products/materials` - Get available materials
- `POST /api/products/generate-caption` - AI caption generation
- `POST /api/products/recommend-price` - AI price recommendation
- `POST /api/products/upload` - Upload new product

### Admin Routes
- `POST /api/admin/login` - Admin login
- `GET /api/admin/artisans` - List artisans
- `POST /api/admin/artisans/:id/verify` - Verify/reject artisan
- `GET /api/admin/stats` - Dashboard statistics

## AI Features

### Caption Generator
Uses template-based NLP with dynamic elements:
- 8 different marketing templates
- Material-aware descriptions
- Artisan name and location integration
- Time investment highlighting

### Price Recommender
Rule-based pricing algorithm considering:
- Base material prices (₹200 - ₹1200)
- Hourly labor rate (₹50/hour)
- Handmade premium (30%)
- Quality multiplier for extended work

## Troubleshooting

### Backend not starting?
- Ensure Python 3.8+ is installed: `python --version`
- Install dependencies: `pip install -r requirements.txt`
- Check if port 5000 is available

### Frontend not connecting to backend?
- Ensure backend is running on port 5000
- Check browser console for CORS errors
- Try refreshing the page

### Images not loading?
- Demo products use placeholder images
- Actual uploaded images are stored in `backend/uploads/products/`

## Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python Flask |
| Database | SQLite |
| Authentication | JWT (JSON Web Tokens) |
| AI/ML | Rule-based + Template-based NLP |

## License

This is an academic/demonstration project. Not intended for production use.

---

Made with ❤️ for Indian Artisans
