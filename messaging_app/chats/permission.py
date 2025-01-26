from rest_framework.permissions import BasePermission

class IsConversationParticipant(BasePermission):
    """
    Custom permission to ensure users can only access conversations they are a part of.
    """
    def has_object_permission(self, request, obj):
        return obj.participants.filter(id=request.user.id).exists()

class IsMessageSender(BasePermission):
    def has_object_permission(self, request, obj):
        return request.user == obj.sender