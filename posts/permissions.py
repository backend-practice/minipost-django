from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsOwnerOrReadonly(permissions.BasePermission):
    """
    只有作者可以编辑
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and obj.owner == request.user
