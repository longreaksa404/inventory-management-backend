![Python](https://img.shields.io/badge/python-3.11-blue)
![Django](https://img.shields.io/badge/django-4.2-green)
![License](https://img.shields.io/badge/license-MIT-orange)

# Inventory Management System (Backend)

A production-ready **Inventory Management System backend** built with Django REST Framework.  
Handles **multi-warehouse inventory**, **orders**, **stock tracking**, and **role-based access control**.  
Focuses on **real-world backend architecture**, not just CRUD.

---

## 🚀 Overview
Manages products, suppliers, warehouses, stock movements, orders, and reporting.  
Suitable for portfolio projects, interviews, and small-medium businesses.  

Key goals:
- Clean domain separation (apps)
- Secure authentication & authorization
- Scalable structure for future growth

---

## 🔑 Key Features
- **Authentication & Authorization**: JWT, refresh tokens, role-based access  
- **User & Role Management**: CRUD, role assignment, activity logging  
- **Inventory Management**: CRUD products & categories, SKU enforcement, archiving  
- **Warehouse & Stock Tracking**: Multiple locations, stock transfers, transaction history  
- **Supplier & Order Management**: CRUD suppliers, purchase & sales orders  
- **Reporting**: Inventory valuation, low-stock alerts, audit trails  

> Full API documentation is available via Swagger.

---

## 🛠 Tech Stack
- **Backend**: Django & Django REST Framework  
- **Authentication**: JWT  
- **Database**: PostgreSQL (recommended)  
- **Async (planned)**: Celery + Redis  
- **Testing (planned)**: Pytest / Django TestCase  
- **Deployment-ready**: Docker (planned)

---

## ⚙️ Setup & Installation
```bash
git clone https://github.com/your-username/inventory-management-backend.git
cd inventory-management-backend

pipenv install
pipenv shell

# Run migrations and create admin user
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Environment Variables
Create a `.env` file:
```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/dbname
```
## 🧭 Roadmap

- [x] Core inventory & order system
- [x] Role-based access control
- [x] Stock transaction history
- [x] Service layer for workflows
- [ ] Password reset & change
- [ ] Celery & notifications
- [ ] Report export (CSV / Excel)
- [ ] OAuth2
- [ ] Automated testing
- [ ] Minimal admin dashboard

---
