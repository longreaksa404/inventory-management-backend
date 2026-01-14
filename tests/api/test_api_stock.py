import pytest


@pytest.mark.django_db
def test_admin_can_create_product(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        '/api/products/',
        {
            'name': 'Test Product',
            'sku': 'Test SKU',
            'stock': 0
        },
        format="json"
    )
    assert response.status_code == 201
    assert response.data["name"] == "Test Product"


# failure test for normal user
@pytest.mark.django_db
def test_normal_user_cannot_create_product(api_client, normal_user):
    api_client.force_authenticate(user=normal_user)

    response = api_client.post(
        "/api/products/",
        {
            "name": "Mouse",
            "sku": "MS001"
        },
        format="json"
    )

    assert response.status_code == 403


# stock in
@pytest.mark.django_db
def test_stock_in_api(product, api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        f"/api/products/{product.id}/stock/in/",
        {"quantity": 10},
        format="json"
    )

    assert response.status_code == 200
    assert response.data["stock"] == 10


# stock out
@pytest.mark.django_db
def test_stock_out_api(product, api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    product.increase_stock(20, user=admin_user)

    response = api_client.post(
        f"/api/products/{product.id}/stock/out/",
        {"quantity": 5},
        format="json"
    )

    assert response.status_code == 200
    assert response.data["stock"] == 15

# failure testing for out more than available
@pytest.mark.django_db
def test_stock_out_more_than_available(product, api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        f"/api/products/{product.id}/stock/out/",
        {"quantity": 5},
        format="json"
    )

    assert response.status_code == 400

@pytest.mark.django_db
def test_adjust_stock_api(product, api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    response = api_client.post(
        f"/api/products/{product.id}/stock/adjust/",
        {
            "quantity": 5,
            "reason": "Inventory audit"
        },
        format="json"
    )

    assert response.status_code == 200
    assert response.data["stock"] == 5

# failure test adjust for normal user
@pytest.mark.django_db
def test_non_admin_adjust_stock_forbidden(product, api_client, normal_user):
    api_client.force_authenticate(user=normal_user)

    response = api_client.post(
        f"/api/products/{product.id}/stock/adjust/",
        {
            "quantity": 5,
            "reason": "Hack"
        },
        format="json"
    )

    assert response.status_code == 403
