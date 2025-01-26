from rest_framework import permissions

class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to allow only conversation participants to access it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsMessageParticipant(permissions.BasePermission):
    """
    Custom permission to allow only conversation participants to access messages.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.conversation.participants.all()