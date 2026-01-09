import pytest

@pytest.mark.django_db
def test_sales_order_total(sales_order, sales_order_item):
    sales_order.total_amount = (
        sales_order_item.quantity * sales_order_item.unit_price
    )
    sales_order.save()
    sales_order.refresh_from_db()

    assert sales_order.total_amount == 2000
