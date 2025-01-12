from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Message


# Create your views here.

def delete_user(request, user_id):
    """
    View to delete a user account and clean up related data.
    """
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect('home')  # Redirect to the home page after deletion

@login_required
def get_threaded_conversation(request, message_id):
    """
    Fetch a message and all its replies recursively, optimized with select_related and prefetch_related.
    """
    def fetch_replies(message):
        replies = message.replies.prefetch_related(
            'sender', 'receiver'
        ).select_related('parent_message', 'sender', 'receiver')
        return [
            {
                'id': reply.id,
                'content': reply.content,
                'sender': reply.sender.username,
                'receiver': reply.receiver.username,
                'timestamp': reply.timestamp,
                'replies': fetch_replies(reply),
            }
            for reply in replies
        ]

    # Ensure the sender is the logged-in user or has access
    root_message = get_object_or_404(
        Message.objects.filter(sender=request.user).select_related('sender', 'receiver', 'parent_message'),
        id=message_id
    )

    conversation = {
        'id': root_message.id,
        'content': root_message.content,
        'sender': root_message.sender.username,
        'receiver': root_message.receiver.username,
        'timestamp': root_message.timestamp,
        'replies': fetch_replies(root_message),
    }

    return JsonResponse(conversation, safe=False)

@cache_page(60)  # Cache the view for 60 seconds
@login_required
def unread_messages(request):
    """
    Retrieve all unread messages for the logged-in user.
    """
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id', 'sender', 'content', 'timestamp'
    )
    data = [
        {
            'id': message.id,
            'sender': message.sender.username,
            'content': message.content,
            'timestamp': message.timestamp,
        }
        for message in unread_messages
    ]
    return JsonResponse(data, safe=False)