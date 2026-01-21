import pytest
from django.core import mail
from apps.inventory.tasks import notify_low_stock
from apps.inventory.models import Product, Category
from unittest.mock import patch
from celery.exceptions import Retry

@pytest.mark.django_db
def test_notify_low_stock_sends_email():
    category = Category.objects.create(name="Default Category")
    Product.objects.create(
        name="Keyboard",
        sku="KB001",
        quantity=3,
        price=10,
        category=category
    )

    result = notify_low_stock.apply()

    assert result.get().startswith("Low stock notification sent")
    assert len(mail.outbox) == 1
    assert "Keyboard" in mail.outbox[0].body


@pytest.mark.django_db
def test_notify_low_stock_no_products():
    category = Category.objects.create(name="Default Category")
    Product.objects.create(
        name="Mouse",
        sku="MS001",
        quantity=20,
        price=5,
        category=category
    )

    result = notify_low_stock.apply()

    assert result.get() == "No low stock products today."
    assert len(mail.outbox) == 0


# failure task retries
@pytest.mark.django_db
@patch("apps.inventory.tasks.send_mail")
def test_notify_low_stock_retry(mock_send_mail):
    mock_send_mail.side_effect = Exception("SMTP down")

    category = Category.objects.create(name="Default Category")
    Product.objects.create(
        name="Monitor",
        sku="MN001",
        quantity=2,
        price=200,
        category=category,
    )

    with pytest.raises(Exception):
        notify_low_stock()

@pytest.mark.django_db
@patch("apps.inventory.tasks.send_mail")
def test_notify_low_stock_email_mocked(mock_send_mail):
    category = Category.objects.create(name="Default Category")
    Product.objects.create(
        name="Camera",
        sku="CM001",
        quantity=1,
        price=500,
        category=category
    )

    notify_low_stock.apply()

    mock_send_mail.assert_called_once()


from unittest.mock import patch
