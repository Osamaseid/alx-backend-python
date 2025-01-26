from django.contrib import admin
from .models import Message, CustomUser, Conversation

admin.site.register((Message, CustomUser, Conversation))