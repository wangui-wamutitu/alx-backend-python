from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.sender == request.user or obj.recipient == request.user
    

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to access related messages.
    """

    def has_permission(self, request, view):
        # Ensure user is authenticated for any API access
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Only participants can view, update, or delete a message
        if request.method in ["GET", "PUT", "PATCH", "DELETE"]:
            return request.user in obj.conversation.participants.all()
        return True  # allow POST or other methods generally
