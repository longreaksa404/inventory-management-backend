# tests/conftest.py
import pytest
from django.contrib.auth.hashers import make_password
from apps.accounts.models import CustomUser
from apps.inventory.models import Category, Product, StockTransaction
from apps.warehouses.models import Warehouse
from apps.suppliers.models import Supplier
from apps.orders.models import PurchaseOrder, PurchaseOrderItem, SalesOrder, SalesOrderItem

# -----------------------------
# Users Fixtures
# -----------------------------
@pytest.fixture
def admin_user(db):
    """Admin user with full permissions"""
    return CustomUser.objects.create(
        username="admin",
        email="admin@example.com",
        password=make_password("password123"),
        role="Admin",
        is_staff=True,
        is_superuser=True
    )

@pytest.fixture
def manager_user(db):
    """Manager user with some elevated permissions"""
    return CustomUser.objects.create(
        username="manager",
        email="manager@example.com",
        password=make_password("password123"),
        role="Manager",
        is_staff=True
    )

@pytest.fixture
def staff_user(db):
    """Regular staff user"""
    return CustomUser.objects.create(
        username="staff",
        email="staff@example.com",
        password=make_password("password123"),
        role="Staff",
        is_staff=False
    )

# -----------------------------
# Inventory Fixtures
# -----------------------------
@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Electronics",
        description="Electronic gadgets and devices"
    )

@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Laptop",
        sku="LAP123",
        price=1000,
        quantity=10,
        status="ACTIVE",
        category=category
    )

@pytest.fixture
def stock_transaction_in(db, product, admin_user, warehouse):
    """Example stock inflow transaction"""
    return StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="IN",
        quantity=5,
        performed_by=admin_user,
        notes="Initial stock"
    )

# -----------------------------
# Warehouses Fixtures
# -----------------------------
@pytest.fixture
def warehouse(db):
    return Warehouse.objects.create(
        name="Main Warehouse",
        location="Phnom Penh",
        capacity=1000
    )

# -----------------------------
# Suppliers Fixtures
# -----------------------------
@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Tech Supplier",
        contact_email="supplier@example.com",
        phone="012345678",
        address="Phnom Penh"
    )

# -----------------------------
# Purchase Order Fixtures
# -----------------------------
@pytest.fixture
def purchase_order(db, supplier, admin_user):
    return PurchaseOrder.objects.create(
        supplier=supplier,
        order_date="2026-01-01",
        status="PENDING",
        total_amount=0,
        created_by=admin_user
    )

@pytest.fixture
def purchase_order_item(db, purchase_order, product):
    return PurchaseOrderItem.objects.create(
        order=purchase_order,
        product=product,
        quantity=5,
        unit_price=product.price
    )

# -----------------------------
# Sales Order Fixtures
# -----------------------------
@pytest.fixture
def sales_order(db, staff_user):
    return SalesOrder.objects.create(
        customer_name="John Doe",
        order_date="2026-01-01",
        status="PENDING",
        total_amount=0,
        created_by=staff_user
    )

@pytest.fixture
def sales_order_item(db, sales_order, product):
    return SalesOrderItem.objects.create(
        order=sales_order,
        product=product,
        quantity=2,
        unit_price=product.price
    )

# -----------------------------
# Helper Fixtures / Common
# -----------------------------
@pytest.fixture
def login_api_client(admin_user, client):
    """APIClient logged in as admin for integration tests"""
    from rest_framework.test import APIClient
    api_client = APIClient()
    api_client.force_authenticate(user=admin_user)
    return api_client
