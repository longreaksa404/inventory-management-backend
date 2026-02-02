from rest_framework.permissions import BasePermission, SAFE_METHODS
# basepermission for decide if the user is allowed
# SAFE_METHODS standard read only method

# helper func (auth check   )
def has_perm(user, perm):
    if not user or not user.is_authenticated:
        return False
    return user.has_perm(perm)


class CategoryPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return has_perm(request.user, "inventory.view_category")

        if request.method == "POST":
            return has_perm(request.user, "inventory.add_category")

        if request.method in ["PUT", "PATCH"]:
            return has_perm(request.user, "inventory.change_category")

        if request.method == "DELETE":
            return has_perm(request.user, "inventory.delete_category")

        return False


class ProductPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return has_perm(request.user, "inventory.view_product")

        if request.method == "POST":
            return has_perm(request.user, "inventory.add_product")

        if request.method in ["PUT", "PATCH"]:
            return has_perm(request.user, "inventory.change_product")

        if request.method == "DELETE":
            return has_perm(request.user, "inventory.delete_product")

        return False


class StockTransactionPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return (
                    has_perm(request.user, "inventory.view_stocktransaction")
                    or has_perm(request.user, "inventory.view_stock_history")
            )

        if request.method == "POST":
            return has_perm(request.user, "inventory.create_stock_transaction")

        if request.method in ["PUT", "PATCH", "DELETE"]:
            return has_perm(request.user, "inventory.approve_stock_transaction")

        return False


class LowStockAlertPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return has_perm(request.user, "inventory.view_low_stock_alert")

        if request.method in ["PUT", "PATCH"]:
            return has_perm(request.user, "inventory.resolve_low_stock_alert")

        return False


class ProductActionPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == "discontinue":
            return has_perm(request.user, "inventory.discontinue_product")

        if view.action == "adjust_stock":
            return has_perm(request.user, "inventory.adjust_stock")

        return True
