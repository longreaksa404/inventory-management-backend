from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.orders.models import SaleOrder, PurchaseOrder
from apps.inventory.models import LowStockAlert
from apps.reports.models import SalesReportEntry, PurchaseReportEntry, StockReportEntry


@receiver(post_save, sender=SaleOrder)
def create_sales_report_entry(sender, instance, **kwargs):
    if instance.status == "completed":
        total = getattr(instance, "total_amount", None)
        if total is None:
            total = sum(item.quantity * item.unit_price for item in instance.items.all())
        SalesReportEntry.objects.get_or_create(
            order=instance,
            defaults={"total_amount": total}
        )


@receiver(post_save, sender=PurchaseOrder)
def create_purchase_report_entry(sender, instance, **kwargs):
    if instance.status == "received":
        total = getattr(instance, "total_amount", None)
        if total is None:
            total = sum(item.quantity * item.unit_price for item in instance.items.all())
        PurchaseReportEntry.objects.get_or_create(
            order=instance,
            defaults={"total_cost": total}
        )


@receiver(post_save, sender=LowStockAlert)
def create_stock_report_entry(sender, instance, **kwargs):
    StockReportEntry.objects.get_or_create(
        alert=instance,
        defaults={
            "product_name": instance.product.name,
            "quantity": instance.quantity,
        }
    )
