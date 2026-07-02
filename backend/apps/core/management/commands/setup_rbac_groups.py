"""
Creates/updates the Staff, Manager, and Admin permission groups from a
single source of truth. Safe to re-run — uses get_or_create and always
overwrites the permission set to match this file exactly.

Usage:
    python manage.py setup_rbac_groups
    python manage.py setup_rbac_groups --dry-run
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


# Each entry: "app_label.codename"
STAFF_PERMS = [
    "inventory.view_category",
    "inventory.view_product",
    "inventory.view_stocktransaction",
    "inventory.view_stock_history",
    "inventory.create_stock_transaction",
    "inventory.view_low_stock_alert",
    "suppliers.view_supplier",
    "warehouses.view_warehouse",
    "orders.view_purchaseorder",
    "orders.add_purchaseorder",
    "orders.confirm_purchase_order",
    "orders.receive_purchase_order",
    "orders.view_purchaseorderitem",
    "orders.view_saleorder",
    "orders.add_saleorder",
    "orders.confirm_sale_order",
    "orders.ship_sale_order",
    "orders.invoice_sale_order",
    "orders.view_saleorderitem",
    "orders.view_orderstatushistory",
]

MANAGER_EXTRA_PERMS = [
    "inventory.add_category",
    "inventory.change_category",
    "inventory.view_cost_price",
    "inventory.approve_stock_transaction",
    "inventory.resolve_low_stock_alert",
    "suppliers.add_supplier",
    "suppliers.change_supplier",
    "warehouses.add_warehouse",
    "warehouses.change_warehouse",
    "orders.change_purchaseorder",
    "orders.change_saleorder",
    "accounts.manage_customers",
    "reports.view_reports",
]

ADMIN_EXTRA_PERMS = [
    "inventory.delete_category",
    "inventory.delete_product",
    "inventory.adjust_stock",
    "inventory.discontinue_product",
    "inventory.delete_stocktransaction",
    "suppliers.delete_supplier",
    "warehouses.delete_warehouse",
    "orders.delete_purchaseorder",
    "orders.cancel_purchase_order",
    "orders.delete_saleorder",
    "orders.cancel_sale_order",
    "orders.add_purchaseorderitem",
    "orders.change_purchaseorderitem",
    "orders.delete_purchaseorderitem",
    "orders.add_saleorderitem",
    "orders.change_saleorderitem",
    "orders.delete_saleorderitem",
    "orders.add_orderstatushistory",
]

GROUPS = {
    "Staff": STAFF_PERMS,
    "Manager": STAFF_PERMS + MANAGER_EXTRA_PERMS,
    "Admin": STAFF_PERMS + MANAGER_EXTRA_PERMS + ADMIN_EXTRA_PERMS,
}


class Command(BaseCommand):
    help = "Creates/updates the Staff, Manager, and Admin RBAC groups."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would change without saving anything.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        for group_name, codenames in GROUPS.items():
            perms = []
            missing = []

            for entry in codenames:
                app_label, codename = entry.split(".", 1)
                try:
                    perm = Permission.objects.get(
                        content_type__app_label=app_label, codename=codename
                    )
                    perms.append(perm)
                except Permission.DoesNotExist:
                    missing.append(entry)

            if missing:
                self.stdout.write(
                    self.style.WARNING(
                        f"[{group_name}] Skipping missing codenames: {', '.join(missing)}"
                    )
                )

            if dry_run:
                self.stdout.write(
                    f"[DRY RUN] {group_name}: would assign {len(perms)} permissions"
                )
                continue

            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.set(perms)
            action = "Created" if created else "Updated"
            self.stdout.write(
                self.style.SUCCESS(f"{action} '{group_name}' with {len(perms)} permissions")
            )

        if not dry_run:
            self.stdout.write(self.style.SUCCESS("\nDone. Assign users via /admin/auth/user/ → Groups field."))