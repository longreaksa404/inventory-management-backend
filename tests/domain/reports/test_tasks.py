import pytest
from apps.reports.tasks import generate_inventory_report
from apps.inventory.models import Product

@pytest.mark.django_db
def test_generate_inventory_report():
    Product.objects.create(
        name="Printer",
        sku="PR001",
        quantity=2,
        price=200
    )

    result = generate_inventory_report.delay()
    data = result.get()

    assert data["total_products"] == 1
    assert data["low_stock"] == 1
