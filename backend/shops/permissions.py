from rest_framework.permissions import BasePermission


class IsOwnerOfShop(BasePermission):
    def has_object_permission(self, request, view, obj):
        # اگر کاربر لاگین نیست
        if not request.user or not request.user.is_authenticated:
            return False

        # obj اینجا Product هست
        return obj.shop.owner == request.user