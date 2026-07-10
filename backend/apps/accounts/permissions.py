# apps/accounts/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class CustomerPermission(BasePermission):
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