import pytest
from apps.inventory.models import Product, Category
from apps.reports.tasks import generate_inventory_report


@pytest.mark.django_db
def test_generate_inventory_report():
    category = Category.objects.create(
        name="Office Equipment",
        description="Printers, scanners, and copiers"
    )

    Product.objects.create(
        name="Printer",
        sku="PR001",
        quantity=2,
        price=200,
        category=category,
        status="active"
    )

    report = generate_inventory_report()
    assert report["total_products"] == 1
    assert report["low_stock"] == 1
