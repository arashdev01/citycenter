from rest_framework import serializers
from .models import Shop, Product, Category, Order, OrderItem


# --------------------
# Shop
# --------------------
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


# --------------------
# Product
# --------------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


# --------------------
# Category
# --------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# --------------------
# Order Item
# --------------------
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]
        read_only_fields = ["price"]


# --------------------
# Order
# --------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "shop",
            "status",
            "total_price",
            "items",
            "created_at",
        ]
        read_only_fields = ["user", "created_at", "total_price"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)

        total = 0

        for item in items_data:
            product = item["product"]
            quantity = item.get("quantity", 1)

            price = product.price * quantity

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=price,
            )

            total += price

        order.total_price = total
        order.save()

        return order