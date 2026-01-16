from django.db import transaction
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from apps.orders.models import SaleOrder, PurchaseOrder, OrderStatusHistory
from apps.orders.serializers import PurchaseOrderSerializer, SalesOrderSerializer
from apps.orders.tasks import process_sales_order_shipping, process_purchase_order_receiving
from rest_framework.permissions import IsAuthenticated
from apps.orders.permissions import SaleOrderPermission, PurchaseOrderPermission


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
    permission_classes = [IsAuthenticated, PurchaseOrderPermission]

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
    def receive(self, request, pk=None):
        order = self.get_object()

        if order.status != "confirmed":
            return Response(
                {"detail": "Only confirmed orders can be received"},
                status=status.HTTP_400_BAD_REQUEST
            )

        process_purchase_order_receiving.delay(order.id, request.user.id)

        return Response(
            {"detail": "Purchase order receiving started"},
            status=status.HTTP_202_ACCEPTED
        )


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all().select_related('customer', 'warehouse')
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated, SaleOrderPermission]

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
    def ship(self, request, pk=None):
        order = self.get_object()

        if order.status != "confirmed":
            return Response(
                {"detail": "Only confirmed orders can be shipped"},
                status=status.HTTP_400_BAD_REQUEST
            )

        process_sales_order_shipping.delay(order.id, request.user.id)

        return Response(
            {"detail": "Shipping started"},
            status=status.HTTP_202_ACCEPTED
        )

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
            for item in instance.items.all():
                product = item.product
                if product.quantity < item.quantity:
                    raise ValidationError(
                        f"Not enough stock for {product.name} "
                        f"(needed {item.quantity}, available {product.quantity})"
                    )
        return super().update(request, *args, **kwargs)
