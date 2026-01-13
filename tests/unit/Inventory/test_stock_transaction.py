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


@pytest.mark.django_db
def test_stock_increase_on_receive(product, admin_user):
    product.increase_stock(10, user=admin_user)

    product.refresh_from_db()
    assert product.stock == 10


@pytest.mark.django_db
def test_stock_decrease_on_issue(product, admin_user):
    product.increase_stock(20, user=admin_user)
    product.decrease_stock(5, user=admin_user)

    product.refresh_from_db()
    assert product.stock == 15


@pytest.mark.django_db
def test_adjust_stock_increase(product, admin_user):
    product.adjust_stock(5, reason="Inventory correction", user=admin_user)

    product.refresh_from_db()
    assert product.stock == 5


@pytest.mark.django_db
def test_adjust_stock_negative_not_allowed(product, admin_user):
    with pytest.raises(ValidationError):
        product.adjust_stock(-10, reason="Invalid adjustment", user=admin_user)


@pytest.mark.django_db
def test_non_admin_cannot_adjust_stock(product, normal_user):
    with pytest.raises(PermissionError):
        product.adjust_stock(10, reason="Hack attempt", user=normal_user)
