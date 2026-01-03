from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.reports.models import LowStockAlert, StockReportEntry

@receiver(post_save, sender=LowStockAlert)
def create_stock_report_entry(sender, instance, **kwargs):
    print("Reports signal fired for LowStockAlert", instance.id)
    StockReportEntry.objects.get_or_create(
        alert=instance,
        defaults={
            "product_name": instance.product.name,
            # ✅ use reorder_level or compute net stock elsewhere
            "quantity": instance.reorder_level,
        }
    )
