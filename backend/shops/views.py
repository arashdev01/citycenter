from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Shop, Product, Category, Order
from .serializers import (
    ShopSerializer,
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
)
from .permissions import IsOwnerOfShop


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(owner=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOfShop]

    def get_queryset(self):
        queryset = Product.objects.all()

        shop_id = self.request.query_params.get('shop')
        category_id = self.request.query_params.get('category')

        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def perform_create(self, serializer):
        user = self.request.user

        if not user.is_authenticated:
            raise PermissionDenied("Login required")

        shop = serializer.validated_data.get('shop')
        category = serializer.validated_data.get('category')

        if shop.owner != user:
            raise PermissionDenied("This shop is not yours")

        if category and category.shop != shop:
            raise PermissionDenied("Category does not belong to this shop")

        serializer.save()


@api_view(['GET'])
def shop_detail(request, unit_number):
    shop = get_object_or_404(Shop, unit_number=unit_number)
    serializer = ShopSerializer(shop)
    return Response(serializer.data)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Category.objects.all()

        shop_id = self.request.query_params.get('shop')

        if shop_id:
            queryset = queryset.filter(shop_id=shop_id)

        return queryset
    def perform_create(self, serializer):
        user = self.request.user
        shop = serializer.validated_data.get('shop')

        if shop.owner != user:
            raise PermissionDenied("This shop is not yours")

        serializer.save()


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Order.objects.none()

        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)