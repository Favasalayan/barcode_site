from rest_framework import serializers
from .models import Product, Scanhistory


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ScanHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Scanhistory
        fields = "__all__"