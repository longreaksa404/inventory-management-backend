from django.db import transaction
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from apps.orders.models import SaleOrder, PurchaseOrder, OrderStatusHistory
from apps.orders.serializers import PurchaseOrderSerializer, SalesOrderSerializer

def log_status_change(order, old_status, new_status, user):
    from apps.orders.models import OrderStatusHistory
    OrderStatusHistory.objects.create(
        order_type=order.__class__.__name__.lower(),
        order_id=order.id,
        old_status=old_status,
        new_status=new_status,
        changed_by=user
    )

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all().select_related('supplier', 'warehouse')
    serializer_class = PurchaseOrderSerializer

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.status != "draft":
            return Response({"detail": "Only draft orders can be confirmed"}, status=status.HTTP_400_BAD_REQUEST)
        old_status = order.status
        order.status = "confirmed"
        order.save()
        log_status_change(order, old_status, order.status, request.user)
        return Response({"detail": "Confirmed order"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def receive(self, request, pk=None):
        order = self.get_object()
        try:
            order.receive()
            return Response({"detail": "Purchase order received and stock updated."})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all().select_related('customer', 'warehouse')
    serializer_class = SalesOrderSerializer

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.status != 'draft':
            return Response({"detail": "Only draft orders can be confirmed."},
                            status=status.HTTP_400_BAD_REQUEST)
        order.status = 'confirmed'
        order.save()
        return Response({"detail": "Sales order confirmed."})

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def ship(self, request, pk=None):
        order = self.get_object()
        try:
            old_status = order.status
            order.ship()
            log_status_change(order, old_status, order.status, request.user)
            return Response({"detail": "Sales order shipped and stock deducted."})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    @transaction.atomic
    def invoice(self, request, pk=None):
        order = self.get_object()
        if order.status != 'shipped':
            return Response({"detail": "Only shipped orders can be invoiced."},
                            status=status.HTTP_400_BAD_REQUEST)
        order.status = 'invoiced'
        order.save()
        return Response({"detail": "Sales order invoiced."})

    def log_status_change(order, old_status, new_status, user):
        OrderStatusHistory.objects.create(
            order_type=order.__class__.__name__.lower(),
            order_id=order.id,
            old_status=old_status,
            new_status=new_status,
            changed_by=user
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.data.get("status") == "completed":
            # Only validate stock, do not deduct here
            for item in instance.items.all():
                product = item.product
                if product.quantity < item.quantity:
                    raise ValidationError(
                        f"Not enough stock for {product.name} "
                        f"(needed {item.quantity}, available {product.quantity})"
                    )
        return super().update(request, *args, **kwargs)



