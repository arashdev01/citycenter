from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Shop, Product
from .serializers import ShopSerializer, ProductSerializer


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


@api_view(['GET'])
def shop_detail(request, unit_number):
    shop = get_object_or_404(Shop, unit_number=unit_number)
    serializer = ShopSerializer(shop)
    return Response(serializer.data)