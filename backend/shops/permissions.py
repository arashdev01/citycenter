from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOfShop(BasePermission):
    def has_object_permission(self, request, view, obj):
        # اگر کاربر فقط می‌خواد محصول رو ببینه، بهش اجازه بده
        if request.method in SAFE_METHODS:
            return True
            
        # اگر می‌خواد محصول رو تغییر بده یا پاک کنه، باید حتماً صاحب مغازه باشه
        if not request.user or not request.user.is_authenticated:
            return False

        return obj.shop.owner == request.user