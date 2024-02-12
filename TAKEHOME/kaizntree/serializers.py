# serializers.py

from rest_framework import serializers
from .models import Items

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['sku', 'name', 'category', 'stock_status', 'available_stock']
