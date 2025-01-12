from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from .managers import UnreadMessagesManager

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )
    read = models.BooleanField(default=False)  # Tracks if the message has been read

    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager for unread messages

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='edited_messages')  # New field
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for Message {self.message.id}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"
