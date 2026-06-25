# 🛍️ ShopNest — Django E-Commerce Website

A full-featured e-commerce platform built with Django.

## Features
- 🏠 Homepage with hero, featured products, categories, and new arrivals
- 🛍️ Product listing with filters (category, price, sort) and search
- 📄 Product detail page with reviews and ratings
- 🛒 Shopping cart (works for guests and logged-in users)
- 👤 User registration, login, and profile management
- 📦 Order checkout with shipping info and payment method
- 📋 Order tracking with status timeline
- ❌ Order cancellation
- 🔧 Admin panel for products, categories, and orders

## Quick Start

### 1. Install dependencies
```bash
pip install django pillow
```

### 2. Run migrations
```bash
python manage.py migrate
```

### 3. Create admin user
```bash
python manage.py createsuperuser
```

### 4. Start the server
```bash
python manage.py runserver
```

### 5. Open in browser
- Site: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Default Admin Credentials (sample)
- Username: `admin`
- Password: `admin123`
- ⚠️ Change this before deploying!

## Project Structure
```
ecommerce_project/
├── core/           # Settings, main URLs
├── store/          # Products, categories, cart
├── accounts/       # User auth & profiles
├── orders/         # Checkout, order management
├── templates/      # All HTML templates
├── static/         # CSS, JS, images
└── media/          # User-uploaded files
```

## Admin Panel
Manage everything from `/admin/`:
- **Categories** — Add/edit product categories
- **Products** — Add products with images, prices, discounts, stock
- **Orders** — View and update order status
- **Users** — Manage user accounts

## Key URLs
| URL | Description |
|-----|-------------|
| `/` | Homepage |
| `/products/` | All products (with filters) |
| `/product/<slug>/` | Product detail + reviews |
| `/cart/` | Shopping cart |
| `/orders/checkout/` | Checkout |
| `/orders/my-orders/` | Order history |
| `/accounts/login/` | Login |
| `/accounts/register/` | Register |

## Customization
- Change store name: Update "ShopNest" in `templates/base.html`
- Add payment gateway: Extend `orders/views.py` checkout view
- Change colors: Update CSS variables in `templates/base.html`
