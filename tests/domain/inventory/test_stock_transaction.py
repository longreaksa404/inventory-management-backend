import pytest
from apps.inventory.models import StockTransaction
from django.core.exceptions import ValidationError


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
    # Initial fixture quantity = 10, after IN +5 → 15
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
    # Initial fixture quantity = 10, after OUT -3 → 7
    assert product.quantity == 7


@pytest.mark.django_db
def test_stock_adjust_sets_exact_quantity(product, warehouse, admin_user):
    # Current quantity = 10 (from fixture)
    StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="ADJ",
        quantity=7,
        performed_by=admin_user,
        notes="Stock audit correction"
    )
    product.refresh_from_db()
    # ADJ should SET quantity, not add/subtract
    assert product.quantity == 7


@pytest.mark.django_db
def test_stock_increase_on_receive(product, warehouse, admin_user):
    StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="IN",
        quantity=10,
        performed_by=admin_user,
        notes="Stock received"
    )
    product.refresh_from_db()
    # Initial 10 + 10 → 20
    assert product.quantity == 20


@pytest.mark.django_db
def test_stock_decrease_on_issue(product, warehouse, admin_user):
    # First add stock
    StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="IN",
        quantity=20,
        performed_by=admin_user
    )
    # Then issue stock
    StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="OUT",
        quantity=5,
        performed_by=admin_user
    )
    product.refresh_from_db()
    # Initial 10 +20 -5 → 25
    assert product.quantity == 25


@pytest.mark.django_db
def test_adjust_stock_increase(product, warehouse, admin_user):
    StockTransaction.objects.create(
        product=product,
        warehouse=warehouse,
        transaction_type="ADJ",
        quantity=5,
        performed_by=admin_user,
        notes="Inventory correction"
    )
    product.refresh_from_db()
    # ADJ sets quantity exactly to 5
    assert product.quantity == 5


@pytest.mark.django_db
def test_adjust_stock_negative_not_allowed(product, warehouse, admin_user):
    with pytest.raises(ValidationError):
        StockTransaction.objects.create(
            product=product,
            warehouse=warehouse,
            transaction_type="ADJ",
            quantity=-10,
            performed_by=admin_user,
            notes="Invalid adjustment"
        )


@pytest.mark.django_db
def test_non_admin_cannot_adjust_stock(product, warehouse, normal_user):
    with pytest.raises(PermissionError):
        StockTransaction.objects.create(
            product=product,
            warehouse=warehouse,
            transaction_type="ADJ",
            quantity=10,
            performed_by=normal_user,
            notes="Hack attempt"
        )
