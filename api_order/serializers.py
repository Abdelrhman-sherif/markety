from rest_framework import serializers
from .models import Order, OrderItem, Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'quantity', 'price', 'subtotal']

    def get_subtotal(self, obj):
        return obj.quantity * obj.price

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'full_name', 'email', 'address', 'city', 'phone', 'status', 'created_at', 'total', 'items']
