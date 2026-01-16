import pytest
from apps.reports.models import LowStockAlert, StockReportEntry
from apps.inventory.models import Product, Category
from apps.warehouses.models import Warehouse


@pytest.mark.django_db
def test_stock_report_entry_created_on_alert():
    warehouse = Warehouse.objects.create(name="Main Warehouse", location="Phnom Penh")
    category = Category.objects.create(name="Default Category")
    product = Product.objects.create(
        name="SSD",
        sku="SSD001",
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

    entry = StockReportEntry.objects.get(alert=alert)

    assert entry.product_name == "SSD"
    assert entry.quantity == 5


@pytest.mark.django_db
def test_stock_report_entry_not_duplicated():
    warehouse = Warehouse.objects.create(name="Main Warehouse", location="Phnom Penh")
    category = Category.objects.create(name="Default Category")
    product = Product.objects.create(
        name="RAM",
        sku="RAM001",
        quantity=1,
        price=50,
        category=category
    )

    alert = LowStockAlert.objects.create(
        product=product,
        warehouse=warehouse,
        quantity=product.quantity,
        reorder_level=4
    )

    alert.save()

    assert StockReportEntry.objects.filter(alert=alert).count() == 1


@pytest.mark.django_db
def test_low_stock_full_flow():
    warehouse = Warehouse.objects.create(name="Main Warehouse", location="Phnom Penh")
    category = Category.objects.create(name="Default Category")
    product = Product.objects.create(
        name="HDD",
        sku="HD001",
        quantity=2,
        price=80,
        category=category
    )

    alert = LowStockAlert.objects.create(
        product=product,
        warehouse=warehouse,
        quantity=product.quantity,
        reorder_level=5
    )

    report = StockReportEntry.objects.get(alert=alert)

    assert report.product_name == "HDD"
