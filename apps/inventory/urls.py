from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryListCreateView,
    CategoryDetailView,
    ProductViewSet,
    ProductListCreateView,
    ProductDetailView,
    StockTransactionListCreateView,
    StockSummaryView,
    StockHistoryView,
    LowStockAlertViewSet,
)


router = DefaultRouter()
router.register(r"products-actions", ProductViewSet, basename="product-actions")
router.register(r"low-stock-alerts", LowStockAlertViewSet, basename="low-stock-alerts")


urlpatterns = [
    # -------- Categories --------
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),

    # -------- Products (CRUD) --------
    path("products/", ProductListCreateView.as_view(), name="product-list-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),

    # -------- Stock --------
    path("transactions/", StockTransactionListCreateView.as_view(), name="transaction-list-create"),
    path("stock-summary/", StockSummaryView.as_view(), name="stock-summary"),
    path("stock-history/<int:product_id>/", StockHistoryView.as_view(), name="stock-history"),

    # -------- ViewSets --------
    path("", include(router.urls)),
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
