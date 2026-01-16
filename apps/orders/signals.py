from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, SaleOrder
from apps.inventory.models import Product


@receiver(post_save, sender=PurchaseOrder)
def update_stock_on_purchase(sender, instance, created, **kwargs):
    if instance.status == "received":
        for item in instance.items.all():
            product = item.product
            product.quantity += item.quantity
            product.save()


@receiver(post_save, sender=SaleOrder)
def update_stock_on_sale(sender, instance, created, **kwargs):
    if instance.status == "completed":
        for item in instance.items.all():
            product = item.product
            product.quantity -= item.quantity
            product.save()
