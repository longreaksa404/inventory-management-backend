import pytest
from apps.inventory.models import Product


@pytest.mark.django_db
def test_create_product(product):
    assert product.name == "Laptop"
    assert product.quantity == 10
    assert product.sku == "LAP123"


@pytest.mark.django_db
def test_product_quantity_update(product):
    product.quantity += 5
    product.save()
    product.refresh_from_db()
    assert product.quantity == 15


@pytest.mark.django_db
def test_product_sku_unique(category):
    Product.objects.create(
        name="Mouse",
        sku="MOU123",
        price=20,
        quantity=5,
        category=category
    )

    with pytest.raises(Exception):
        Product.objects.create(
            name="Keyboard",
            sku="MOU123",
            price=30,
            quantity=5,
            category=category
        )
