from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]  # include fields you want public

class ProductSerializer(serializers.ModelSerializer):
    # Show readable category in responses…
    category = serializers.StringRelatedField(read_only=True)
    # …and accept category id when creating/updating:
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id", "name", "description", "price", "stock", "image",
            "category", "category_id"
        ]
