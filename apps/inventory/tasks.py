from celery import shared_task
from django.core.mail import send_mail
from apps.inventory.models import Product
from django.conf import settings


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def notify_low_stock(self):
    low_stock_products = Product.objects.filter(quantity__lt=5)

    if not low_stock_products.exists():
        return "No low stock products today."

    message_lines = [f"{p.name} (SKU: {p.sku}) → {p.quantity} left" for p in low_stock_products]
    message = "\n".join(message_lines)

    send_mail(
        subject="Low Stock Alert",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=["admin@gmail.com"],
    )

    return f"Low stock notification sent for {low_stock_products.count()} products."
