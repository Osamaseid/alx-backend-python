from django.urls import path
from .views import get_threaded_conversation, unread_messages

urlpatterns = [
    path('conversation/<int:message_id>/', get_threaded_conversation, name='threaded_conversation'),
    path('unread_messages/', unread_messages, name='unread_messages'),

]

# The /conversation/<message_id>/ endpoint retrieves a message and its replies.
