import pytest

# failure test for normal user stock in product
@pytest.mark.django_db
def test_unauthenticated_access_denied(product, api_client):
    response = api_client.post(
        f"/api/products/{product.id}/stock/in/",
        {"quantity": 10},
        format="json"
    )
    assert response.status_code == 401