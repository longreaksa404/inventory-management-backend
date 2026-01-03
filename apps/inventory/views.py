from rest_framework import permissions, generics, filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, StockTransaction, LowStockAlert
from apps.core.permissions import IsStaffOrReadOnly
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    StockTransactionSerializer,
    StockSummarySerializer,
    StockHistorySerializer, LowStockAlertSerializer
)


class SearchFilterOrderingMixin:
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class CategoryListCreateView(SearchFilterOrderingMixin, generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)

    filterset_fields = ['name']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ProductListCreateView(SearchFilterOrderingMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsStaffOrReadOnly,)

    filterset_fields = ['category', 'status']
    search_fields = ['name', 'sku', 'category__name']
    ordering_fields = ['name', 'sku', 'status', 'quantity', 'price', 'created_at']
    ordering = ['-created_at']


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StockTransactionListCreateView(SearchFilterOrderingMixin, generics.ListCreateAPIView):
    queryset = StockTransaction.objects.select_related('product', 'warehouse', 'performed_by')
    serializer_class = StockTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    filterset_fields = ['product', 'warehouse', 'transaction_type', 'performed_by']
    search_fields = ['product__name', 'product__sku', 'warehouse__name', 'notes']
    ordering_fields = ['timestamp', 'quantity', 'product__name']
    ordering = ['-timestamp']


class StockSummaryView(SearchFilterOrderingMixin, generics.ListAPIView):
    serializer_class = StockSummarySerializer

    filterset_fields = ['category', 'status', 'sku']
    search_fields = ['name', 'sku', 'category__name']
    ordering_fields = ['name', 'sku', 'quantity']
    ordering = ['name']

    def get_queryset(self):
        queryset = Product.objects.all()
        warehouse_id = self.request.query_params.get('warehouse')
        if warehouse_id:
            queryset = queryset.filter(stock_transactions__warehouse_id=warehouse_id).distinct()
        return queryset


class StockHistoryView(SearchFilterOrderingMixin, generics.ListAPIView):
    serializer_class = StockHistorySerializer

    filterset_fields = ['transaction_type', 'warehouse', 'performed_by']
    search_fields = ['product__name', 'product__sku', 'notes']
    ordering_fields = ['timestamp', 'quantity']
    ordering = ['-timestamp']

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return StockTransaction.objects.filter(product_id=product_id).order_by('-timestamp')


class LowStockAlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LowStockAlert.objects.all().order_by("-created_at")
    serializer_class = LowStockAlertSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['product', 'created_at']

