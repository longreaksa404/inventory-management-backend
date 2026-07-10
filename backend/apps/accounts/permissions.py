# apps/accounts/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomerPermission(BasePermission):
    """
    - List/retrieve (GET): any authenticated user.
    - Create (POST): requires 'accounts.add_customer' — Group-controlled,
      same as every other model's add_* permission. No longer unconditionally
      open; a staff user's Group must actually grant this in the Django
      admin panel for them to create a customer (including via the Sale
      Order quick-add flow).
    - Update/deactivate (PUT/PATCH/DELETE): requires 'accounts.manage_customers'.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser:
            return True
        if request.method == "POST":
            return request.user.has_perm("accounts.add_customer")
        return request.user.has_perm("accounts.manage_customers")