from django.db import models

from apps.inventory.models import Product, StockTransaction
from apps.warehouses.models import Warehouse


class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contact_name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name', '-created_at']

    def __str__(self):
        return self.name


