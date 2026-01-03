from django.urls import path
from .views import CategoryListCreateView, CategoryDetailView, ProductListCreateView, ProductDetailView, \
    StockTransactionListCreateView, StockSummaryView, StockHistoryView, LowStockAlertViewSet

# Map ViewSet actions manually
low_stock_alert_list = LowStockAlertViewSet.as_view({'get': 'list'})
low_stock_alert_detail = LowStockAlertViewSet.as_view({'get': 'retrieve'})
urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('transactions/', StockTransactionListCreateView.as_view(), name='transaction-list-create'),
    path('stock-summary/', StockSummaryView.as_view(), name='stocks-summary'),
    path('stock-history/<int:product_id>/', StockHistoryView.as_view(), name='stock-history'),
    path('low-stock-alerts/', low_stock_alert_list, name='low-stock-alert-list'),
    path('low-stock-alerts/<int:pk>/', low_stock_alert_detail, name='low-stock-alert-detail'),
]

# use router way
# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import (
#     CategoryViewSet,
#     ProductViewSet,
#     StockTransactionViewSet,
#     StockSummaryView,
#     StockHistoryView,
# )
#
# # Router for standard CRUD
# router = DefaultRouter()
# router.register(r'categories', CategoryViewSet, basename='category')
# router.register(r'products', ProductViewSet, basename='product')
# router.register(r'transactions', StockTransactionViewSet, basename='transaction')
#
# urlpatterns = [
#     # Router-generated endpoints
#     path('', include(router.urls)),
#
#     # Custom endpoints
#     path('stock-summary/', StockSummaryView.as_view(), name='stocks-summary'),
#     path('stock-history/<int:product_id>/', StockHistoryView.as_view(), name='stock-history'),
# ]
