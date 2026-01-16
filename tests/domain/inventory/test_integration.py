import pytest
from django.core import mail
from apps.inventory.models import Product, Category
from apps.reports.models import LowStockAlert
from apps.warehouses.models import Warehouse


@pytest.mark.django_db
def test_low_stock_alert_triggers_email():
    warehouse = Warehouse.objects.create(name="Main Warehouse", location="Phnom Penh")
    category = Category.objects.create(name="Default Category")
    product = Product.objects.create(
        name="Switch",
        sku="SW001",
        quantity=2,
        price=100,
        category=category
    )

    alert = LowStockAlert.objects.create(
        product=product,
        warehouse=warehouse,
        quantity=product.quantity,
        reorder_level=5
    )

    assert len(mail.outbox) == 1
