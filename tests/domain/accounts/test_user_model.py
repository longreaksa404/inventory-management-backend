import pytest


@pytest.mark.django_db
def test_admin_user_role(admin_user):
    assert admin_user.role == "Admin"
    assert admin_user.is_staff
    assert admin_user.is_superuser


@pytest.mark.django_db
def test_staff_user_role(staff_user):
    assert staff_user.role == "Staff"
    assert not staff_user.is_superuser
