from celery import shared_task
from apps.inventory.models import Product


@shared_task
def generate_inventory_report():
    return {
        "total_products": Product.objects.count(),
        "low_stock": Product.objects.filter(quantity__lt=5).count(),
    }
