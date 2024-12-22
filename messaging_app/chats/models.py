from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
from django.db import models

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Custom related_name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Custom related_name
        blank=True,
    )

    REQUIRED_FIELDS = ['first_name', 'last_name']  # Remove 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'users'
        indexes = [models.Index(fields=['email'])]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
