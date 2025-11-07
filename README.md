# Furniture Shop API (Django + DRF + JWT)

This is a backend API for a Furniture E-commerce application built using:

- Django
- Django REST Framework (DRF)
- JWT Authentication (djangorestframework-simplejwt)
- Django Filters
- Pillow (media uploads)
- Celery + Redis (email sending and background tasks)

---

## ✅ Features

### Users (accounts app)
- Custom user model with phone, address, birth date
- Register, Login (JWT authentication)
- User profile endpoint (`/api/profile/`)

### Catalog (shop app)
- Categories (slug, image, description)
- Products (colors, material, multiple images)
- Filtering by category, color, and material
- Featured products

### Cart & Orders
- Add/remove products from cart
- Cart total price and item count
- Create order from cart
- Order history
- Celery email confirmation
- Auto update order status

---

## 📁 Project Structure

