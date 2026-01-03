from rest_framework import permissions

class IsStaffOrReadOnly(permissions.BasePermission):
    """
    Custom permission:
    - SAFE_METHODS (GET, HEAD, OPTIONS) → allowed for everyone
    - Other methods (POST, PUT, PATCH, DELETE) → only staff users
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
