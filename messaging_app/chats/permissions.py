from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Return True if permission is granted, False otherwise.
        return obj.sender == request.user or obj.recipient == request.user
