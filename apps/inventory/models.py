from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.core.exceptions import ValidationError

from apps.warehouses.models import Warehouse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)  # allow empty description
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        # custom plural label
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('discontinued', 'Discontinued'),
        ('out_of_stock', 'Out of Stock'),
    )

    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, validators=[MinValueValidator(0.0)])
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reorder_level = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ('name',)
        # speed booster for queries from database when filter or ordering
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        self.sku = self.sku.strip().upper()
        super().save(*args, **kwargs)


class StockTransaction(models.Model):
    TRANSACTION_STATUS_CHOICES = (
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('ADJ', 'Adjustment'),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_transactions')
    warehouse = models.ForeignKey(Warehouse, on_delete=models.PROTECT, related_name='stock_transactions', default=1)
    transaction_type = models.CharField(max_length=5, choices=TRANSACTION_STATUS_CHOICES, default='IN')
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    # which user perform this transaction
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='stock_transactions',
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.product.name} ({self.quantity})"

    def clean(self):
        """Prevent stock from going negative."""
        if self.transaction_type == 'OUT' and self.product.quantity < self.quantity:
            raise ValidationError("Not enough stock to complete transaction")

    def apply_transaction(self):
        """Update product quantity based on transaction type."""
        if self.transaction_type == 'IN':
            self.product.quantity += self.quantity
        elif self.transaction_type == 'OUT':
            if self.product.quantity < self.quantity:
                raise ValueError("Not enough stock to complete transaction")
            self.product.quantity -= self.quantity
        elif self.transaction_type == 'ADJ':
            self.product.quantity = self.quantity
        self.product.save()

    def save(self, *args, **kwargs):
        """Automatically apply stock changes when saving a transaction."""
        self.full_clean()
        with transaction.atomic():
            super().save(*args, **kwargs)
            self.apply_transaction()

# apps/inventory/models.py
class LowStockAlert(models.Model):
    product = models.ForeignKey("inventory.Product", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert: {self.product.name} - {self.message}"
