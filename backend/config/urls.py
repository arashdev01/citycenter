from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from shops.views import ShopViewSet, ProductViewSet, shop_detail
from shops.register import register

router = DefaultRouter()
router.register('shops', ShopViewSet)
router.register('products', ProductViewSet)

def home(request):
    return HttpResponse("Pasaj is alive 🚀")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('api/', include(router.urls)),
    path('citycenter/<int:unit_number>/', shop_detail),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', register),
]