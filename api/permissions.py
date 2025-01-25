from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsCreaterOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return bool(
            obj.user == request.user
        )