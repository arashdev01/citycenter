from django.db import transaction
from rest_framework import serializers
from .models import Shop, Product, Category, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ShopSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Shop
        fields = "__all__"
        read_only_fields = ["owner"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "price"]
        read_only_fields = ["price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ["id", "user", "shop", "status", "total_price", "items", "created_at"]
        read_only_fields = ["user", "created_at", "total_price"]

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        order = Order.objects.create(**validated_data)
        total = 0

        for item in items_data:
            product = item["product"]
            quantity = item.get("quantity", 1)

            if product.shop != order.shop:
                raise serializers.ValidationError(
                    f"محصول {product.name} متعلق به این مغازه نیست"
                )

            if product.stock < quantity:
                raise serializers.ValidationError(
                    f"موجودی {product.name} کافی نیست"
                )

            price = product.price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)
            product.stock -= quantity
            product.save()
            total += price

        order.total_price = total
        order.save()
        return order