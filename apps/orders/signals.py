from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PurchaseOrder, SaleOrder
from apps.inventory.models import Product

# --- Purchase Order Signal ---
@receiver(post_save, sender=PurchaseOrder)
def update_stock_on_purchase(sender, instance, created, **kwargs):
    """
    When a PurchaseOrder is saved with status 'received',
    increase product stock automatically.
    """
    if instance.status == "received":
        for item in instance.items.all():  # assuming PurchaseOrder has related items
            product = item.product
            product.quantity += item.quantity
            product.save()


# --- Sale Order Signal ---
@receiver(post_save, sender=SaleOrder)
def update_stock_on_sale(sender, instance, created, **kwargs):
    """
    When a SaleOrder is saved with status 'completed',
    decrease product stock automatically.
    """
    if instance.status == "completed":
        for item in instance.items.all():  # assuming SaleOrder has related items
            product = item.product
            product.quantity -= item.quantity
            product.save()
