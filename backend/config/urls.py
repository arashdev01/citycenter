from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from shops.views import OrderViewSet, ProductViewSet, CategoryViewSet, OrderViewSet, shop_detail
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from shops.views import ShopViewSet, ProductViewSet, CategoryViewSet, shop_detail
from shops.register import register


router = DefaultRouter()

router.register('shops', ShopViewSet)
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet, basename='categories')
router.register('orders', OrderViewSet, basename='orders')

def home(request):
    return HttpResponse("Pasaj is alive 🚀")


urlpatterns = [
    path('', home),

    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    path('citycenter/<int:unit_number>/', shop_detail),

    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', register),
]