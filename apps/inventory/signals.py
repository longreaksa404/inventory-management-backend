from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.reports.models import StockReportEntry, LowStockAlert
from django.core.mail import send_mail


@receiver(post_save, sender=LowStockAlert)
def create_stock_report_entry(sender, instance, created, **kwargs):
    if created:
        StockReportEntry.objects.get_or_create(
            alert=instance,
            defaults={
                "product_name": instance.product.name,
                "quantity": instance.reorder_level,
            }
        )
        send_mail(
            subject="Low Stock Alert",
            message=f"{instance.product.name} is low on stock ({instance.quantity}/{instance.reorder_level})",
            from_email="noreply@example.com",
            recipient_list=["admin@gmail.com"],
        )
