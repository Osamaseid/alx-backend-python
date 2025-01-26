from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    password_hash = models.CharField(max_length=255, null=False)
    phone_number = models.CharField(max_length=63, null=True)
    
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('host', 'Host'),
        ('guest', 'Guest'),
    )
    role = models.CharField(max_length=7, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    groups = None
    user_permissions = None

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, null=False)
    participants = models.ManyToManyField(User, related_name='participants')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participants = ', '.join([str(participant) for participant in self.participants.all()])
        return f"Conversation ({self.conversation_id}) with participants {participants}"


class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_body = models.TextField(null=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    sent_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(default=None, null=True)
    conversation = models.ForeignKey('conversation', on_delete=models.CASCADE, related_name='messages')

    def __str__(self):
        return f"Message ({self.message_id}) from {self.sender} in conversation {self.conversation}"