from rest_framework import generics, permissions
from apps.inventory.views import SearchFilterOrderingMixin
from .models import Supplier
from .serializers import SupplierSerializer


class SupplierListCreateView(generics.ListCreateAPIView, SearchFilterOrderingMixin):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    filterset_fields = ['name', 'email']
    search_fields = ['name', 'contact_name', 'email', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)




