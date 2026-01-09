import pytest
from apps.inventory.models import StockTransaction

@pytest.mark.django_db
def test_stock_increases(product, warehouse, admin_user):
    StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="IN",
        quantity=5,
        performed_by=admin_user
    )
    product.refresh_from_db()
    assert product.quantity == 15


@pytest.mark.django_db
def test_stock_decreases(product, warehouse, admin_user):
    StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="OUT",
        quantity=3,
        performed_by=admin_user
    )
    product.refresh_from_db()
    assert product.quantity == 7

import pytest
from apps.inventory.models import StockTransaction

@pytest.mark.django_db
def test_stock_adjust_sets_exact_quantity(product, warehouse, admin_user):
    # Current quantity = 10 (from fixture)

    StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="ADJUST",
        quantity=7,
        performed_by=admin_user,
        notes="Stock audit correction"
    )

    product.refresh_from_db()

    # ADJUST should SET quantity, not add/subtract
    assert product.quantity == 7
