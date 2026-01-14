import pytest
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
def test_login_success(admin_user):
    cliend = APIClient()

    response = cliend.post(
        reverse("token_obtain_pair"),
        {
            "email": admin_user.email,
            "password": "adminadmin",
        },
        format="json"
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

# failure test
def test_login_fail_wrong_password(admin_user):
    cliend = APIClient()

    response = cliend.post(
        reverse("token_obtain_pair"),
        {
            "email": admin_user.email,
            "password": "wrongpassword",
        },
        format="json"
    )

    assert response.status_code == 401