# Furniture Shop Backend

Final project for Women in AI Python/Django course.

This project is a simple furniture shop backend built with **Django** and **Django REST Framework**.  
It supports custom users, product catalog, cart, and orders.

---

## 🧑‍💻 Tech Stack

- Python
- Django
- Django REST Framework
- SQLite (default Django DB)

---

## 👤 Custom User (accounts app)

Custom user model with extra fields:

- `first_name`
- `last_name`
- `phone`
- `address`
- `birth_date`

Method:

- `get_full_name()` – returns `"first_name last_name"`

User is managed in Django admin with additional fields shown.

---

## 🛒 Shop Models (shop app)

### Category
- `name`
- `slug`
- `description`
- `image`
- `is_active`
- `created_at`

### Attribute
Used for product attributes such as color and material.

- `type` – choices: `"color"`, `"material"`
- `value`

### Product
- `category` (ForeignKey to Category)
- `name`
- `slug`
- `description`
- `price`
- `is_featured`
- `stock`
- `created_at`
- `attributes` (ManyToMany to Attribute)
- related images through `ProductImage`

### ProductImage
- `product` (ForeignKey to Product)
- `image`

### Cart & CartItem
- `Cart`:
  - `user`
  - `updated_at`
  - methods: `get_total_price()`, `get_total_items_count()`

- `CartItem`:
  - `cart`
  - `product`
  - `quantity`

### Order & OrderItem
- `Order`:
  - `user`
  - `order_number` (auto generated)
  - `status`
  - `total_amount`
  - `shipping_address`
  - `phone_number`
  - `created_at`
  - `updated_at`

- `OrderItem`:
  - `order`
  - `product`
  - `quantity`
  - `price`

---

## 🔗 API Endpoints

### Accounts

- `POST /accounts/register/`  
  Register a new user.

Example body:

```json
{
  "username": "user1",
  "email": "user@example.com",
  "first_name": "Name",
  "last_name": "Surname",
  "phone": "555123456",
  "address": "Tbilisi",
  "birth_date": "1999-01-01",
  "password": "strongpassword123"
}


