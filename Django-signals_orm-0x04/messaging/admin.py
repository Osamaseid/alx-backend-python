from django.contrib import admin
from .models import Message, Notification

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'timestamp')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('timestamp',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'message', 'is_read', 'timestamp')
    search_fields = ('user__username', 'message__content')
    list_filter = ('is_read', 'timestamp')
