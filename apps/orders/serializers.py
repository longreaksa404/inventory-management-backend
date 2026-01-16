from rest_framework import serializers
from django.db import transaction
from django.conf import settings

from apps.orders.models import (
    PurchaseOrder, PurchaseOrderItem,
    SaleOrder, SaleOrderItem, OrderStatusHistory
)
from apps.inventory.models import Product
from apps.suppliers.models import Supplier


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'notes', 'line_total']

    def get_line_total(self, obj):
        return obj.line_total()


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True, write_only=True)
    items_detail = PurchaseOrderItemSerializer(source='items', many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = [
            'id', 'supplier', 'supplier_name', 'warehouse', 'warehouse_name',
            'status', 'expected_date', 'notes', 'created_at', 'updated_at',
            'created_by', 'items', 'items_detail'
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        for item in value:
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero.")
            if item['unit_price'] < 0:
                raise serializers.ValidationError("Unit price cannot be negative.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = PurchaseOrder.objects.create(created_by=user, **validated_data)
        for item in items_data:
            PurchaseOrderItem.objects.create(order=order, **item)
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                PurchaseOrderItem.objects.create(order=instance, **item)
        return instance


class SalesOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = SaleOrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'unit_price', 'discount', 'notes', 'line_total']

    def get_line_total(self, obj):
        return max((obj.quantity * obj.unit_price) - obj.discount, 0)


class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True, write_only=True)
    items_detail = SalesOrderItemSerializer(source='items', many=True, read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = SaleOrder
        fields = [
            'id', 'customer', 'customer_name', 'warehouse', 'warehouse_name',
            'status', 'order_date', 'shipped_date', 'notes',
            'created_at', 'updated_at', 'created_by',
            'items', 'items_detail'
        ]
        read_only_fields = ['order_date', 'created_at', 'updated_at', 'created_by']

    def validate(self, data):
        if data.get("status") == "completed" and "items" not in data:
            instance = getattr(self, "instance", None)
            if instance:
                for item in instance.items.all():
                    product = item.product
                    if product.quantity < item.quantity:
                        raise serializers.ValidationError(
                            f"Not enough stock for {product.name} "
                            f"(needed {item.quantity}, available {product.quantity})"
                        )

        if data.get("status") == "completed" and "items" in data:
            for item in data["items"]:
                product = item.get("product")
                if isinstance(product, int):
                    product = Product.objects.get(pk=product)
                elif isinstance(product, Product):
                    pass
                else:
                    continue

                if product.quantity < item["quantity"]:
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name} "
                        f"(needed {item['quantity']}, available {product.quantity})"
                    )
        return data

    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError("At least one item is required.")
        for item in value:
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than zero.")
            if item['unit_price'] < 0:
                raise serializers.ValidationError("Unit price cannot be negative.")

            try:
                product = Product.objects.get(
                    pk=item['product'].id if isinstance(item['product'], Product) else item['product'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product {item['product']} does not exist.")
            if product.quantity < item['quantity']:
                raise serializers.ValidationError(f"Not enough stock for {product.name}.")
        return value

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = SaleOrder.objects.create(created_by=user, **validated_data)
        for item in items_data:
            product = item['product']
            if isinstance(product, int):
                product = Product.objects.get(pk=product)
            SaleOrderItem.objects.create(order=order, **item)
        return order

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item in items_data:
                product = item['product']
                if isinstance(product, int):
                    product = Product.objects.get(pk=product)
                SaleOrderItem.objects.create(order=instance, **item)
        return instance


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    changed_by_name = serializers.CharField(source='changed_by.username', read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'order_type', 'order_id', 'old_status', 'new_status', 'changed_by_name', 'changed_at']
