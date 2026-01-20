# Inventory Management System (Backend)

![Python](https://img.shields.io/badge/python-3.12-blue)
![Django](https://img.shields.io/badge/django-5.2-green)
![License](https://img.shields.io/badge/license-MIT-orange)

A **production-ready Inventory Management System backend** built with **Django & Django REST Framework**.  
Designed around **real business workflows**, **clean backend architecture**, and **scalability**, not just CRUD APIs.

This project demonstrates how a **serious backend system** is structured, secured, tested, and prepared for deployment.

---

## 🚀 Overview

This system manages **users, roles, suppliers, warehouses, inventory, orders, and reports** across multiple locations.

It focuses on:
- Real-world domain modeling
- Strong authorization & permissions
- Async processing & background jobs
- Data consistency using transactions
- Production-ready configuration & logging

Built as a **portfolio-grade backend project** suitable for:
- Job applications
- Technical interviews
- Small–medium business systems
- Backend architecture review

---

## 🔑 Key Features

### 🔐 Authentication & Authorization
- JWT authentication (access & refresh tokens)
- Custom user model
- Role-based access control (RBAC)
- Permission checks enforced across all endpoints

### 📦 Inventory & Warehouse Management
- Multi-warehouse stock tracking
- Stock movement history & audit trail
- Low-stock detection
- Data consistency using database transactions

### 🧾 Orders & Suppliers
- Purchase & sales order workflows
- Supplier management
- Order lifecycle & status validation
- Permission-based order operations

### ⚙️ Async & Background Processing
- Celery + Redis for background jobs
- Email notifications handled asynchronously
- Scheduled tasks using Celery Beat
- Task monitoring via Flower

### 🔔 System Automation
- Django signals for side effects
- Automated stock updates
- Notification triggers on key events

### 🧪 Testing & Reliability
- Unit tests for domain logic
- API tests for endpoints
- Async task tests
- **35 passing tests** across unit → API → async layers
- Tests cover critical business flows and failure cases

---

### 🧱 Architecture & Design
- Domain-driven app separation
- Service & transaction boundaries
- Explicit permission and business rule enforcement

---

## 🔌 API Documentation (Swagger)

Interactive API documentation covering:
- Authentication flows
- Inventory & order workflows
- Permissions & error handling

Swagger UI available at:
- `/swagger/`
- `/redoc/`

---

## 🛠 Tech Stack

- **Language**: Python 3.11  
- **Framework**: Django 5.x, Django REST Framework
- **Authentication**: JWT (SimpleJWT)  
- **Database**: PostgreSQL  
- **Async**: Celery + Redis  
- **Task Monitoring**: Flower  
- **Documentation**: drf-yasg (Swagger)  
- **Testing**: Pytest, pytest-django, DRF API tests, async & Celery task tests
- **Configuration**: Environment-based settings  

---

## ⚙️ Setup & Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/longchanreaksa/inventory-management-backend.git
cd inventory-management-backend
```

### 2️⃣ Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Environment variables
```bash
cp .env.example .env
```
Fill in required values (database, secret key, Redis, email).

### 5️⃣ Run migrations & server
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
---

## 🚀 Deployment

- Environment-based configuration
- Production-ready logging
- Compatible with VPS / Railway / Render
- .env secrets are never committed

Live demo: (add after deployment)

---

## 🎯 Purpose of This Project

- This project was built to demonstrate:
- Real backend engineering decisions
- Clean, maintainable Django architecture
- Readiness for production environments
- Ability to handle async workflows and complex domains

This is a production-oriented backend project, not a tutorial or demo app.

---
