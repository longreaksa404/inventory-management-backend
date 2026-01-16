import pytest


@pytest.mark.django_db
def test_purchase_order_total(purchase_order, purchase_order_item):
    purchase_order.total_amount = (
            purchase_order_item.quantity * purchase_order_item.unit_price
    )
    purchase_order.save()
    purchase_order.refresh_from_db()

    assert purchase_order.total_amount == 5000
