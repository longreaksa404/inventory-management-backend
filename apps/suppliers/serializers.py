from rest_framework import serializers
from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'




# last note! continue look at pdf note about validation and ask some questions on telegram noted
# fix database