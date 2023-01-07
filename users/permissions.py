from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        object_owner_field = getattr(obj, 'get_object_owner_field', 'user')
        lookup = object_owner_field.split('__')
        for field in lookup:
            obj = getattr(obj, field)

        if obj == request.user:
            return True
        else:
            return request.user.is_staff or request.user.is_superuser


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)
