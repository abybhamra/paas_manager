from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return request.user and obj.user == request.user


class IsAdminUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)
