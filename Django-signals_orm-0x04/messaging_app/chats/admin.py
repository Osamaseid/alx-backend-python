from django.contrib import admin
from .models import User, Conversation, Message
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "role", "created_at")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("role",)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("conversation_id", "created_at")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_id", "sender", "conversation", "sent_at")
    search_fields = ("message_body",)
