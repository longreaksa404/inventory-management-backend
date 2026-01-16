import pytest
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from apps.accounts.models import CustomUser
from apps.inventory.models import Category, Product, StockTransaction
from apps.warehouses.models import Warehouse
from apps.suppliers.models import Supplier
from apps.orders.models import PurchaseOrder, PurchaseOrderItem, SaleOrder, SaleOrderItem

User = get_user_model()


@pytest.fixture
def admin_user(db):
    return CustomUser.objects.create(
        username="admin",
        email="admin@example.com",
        password=make_password("adminadmin"),
        role="Admin",
        is_staff=True,
        is_superuser=True
    )


@pytest.fixture
def manager_user(db):
    return CustomUser.objects.create(
        username="manager",
        email="manager@example.com",
        password=make_password("password123"),
        role="Manager",
        is_staff=True
    )


@pytest.fixture
def staff_user(db):
    return CustomUser.objects.create(
        username="staff",
        email="staff@example.com",
        password=make_password("password123"),
        role="Staff",
        is_staff=False
    )


@pytest.fixture
def normal_user(db):
    return CustomUser.objects.create(
        username="user",
        email="user@example.com",
        first_name="Test",
        last_name="User",
        phone_number="012345678",
        password=make_password("password123"),
        role="User"
    )


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
        status="active",
        category=category
    )


@pytest.fixture
def stock_transaction_in(db, product, admin_user, warehouse):
    return StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="IN",
        quantity=5,
        performed_by=admin_user,
        notes="Initial stock"
    )


@pytest.fixture
def warehouse(db):
    return Warehouse.objects.create(
        name="Main Warehouse",
        location="Phnom Penh"
    )


@pytest.fixture
def supplier(db):
    return Supplier.objects.create(
        name="Tech Supplier",
        email="supplier@example.com",
        phone="012345678",
        address="Phnom Penh"
    )


@pytest.fixture
def customer(db):
    return Customer.objects.create(
        name="John Doe",
        email="john@example.com",
        phone="012345678"
    )


@pytest.fixture
def purchase_order(db, supplier, admin_user, warehouse):
    return PurchaseOrder.objects.create(
        supplier=supplier,
        warehouse=warehouse,
        expected_date="2026-01-01",
        status="PENDING",
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


@pytest.fixture
def sales_order(db, staff_user, normal_user, warehouse):
    return SaleOrder.objects.create(
        customer=normal_user,
        warehouse=warehouse,
        order_date="2026-01-01",
        status="PENDING",
        created_by=staff_user
    )


@pytest.fixture
def sales_order_item(db, sales_order, product):
    return SaleOrderItem.objects.create(
        order=sales_order,
        product=product,
        quantity=2,
        unit_price=product.price
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def login_api_client(admin_user):
    api_client = APIClient()
    api_client.force_authenticate(user=admin_user)
    return api_client
