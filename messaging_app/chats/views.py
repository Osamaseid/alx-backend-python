from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import User, Message, Conversation
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('conversation', '-sent_at')
    serializer_class = MessageSerializer

    @action(methods=['get'], detail=False)
    def get_all(self, request):
        messages = Message.objects.all().order_by('-sent_at')
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)
    
    @action(methods=['get'], detail=True)
    def get_conversation(self, request, pk=None):
        conversation = Conversation.objects.filter(pk=pk).first()
        if not conversation:
            return Response({'Error': 'Conversation not exists.'}, status=404)
        
        messages = Message.objects.filter(conversation=conversation).order_by('-sent_at')
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def _create(self, request):
        sender_id = request.data.get('sender')
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        if not all([sender_id, conversation_id, message_body]):
            return Response({'Error': 'All fields are required.'}, status=400)
        
        sender = User.objects.filter(pk=sender_id).first()
        conversation = Conversation.objects.filter(pk=conversation_id).first()
        if not all([sender, conversation]):
            return Response({'Error': 'Sender or conversation not exists.'}, status=404)
        
        message = Message.objects.create(sender=sender, conversation=conversation, message_body=message_body)
        dto = self.get_serializer(message).data

        return Response(dto, status=201)


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer

    def get_serializer_context(self):
        """
        Include the request in the context for serializers.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(methods=['get'], detail=False)
    def get_all(self, request):
        conversations = Conversation.objects.all().order_by('-created_at')
        serializer = ConversationSerializer(conversations, many=True)

        return Response(serializer.data)

    @action(methods=['POST'], detail=False)
    def _create(self, request):
        participants_ids = request.data.get('participants', [])

        filters = {
            'participants': participants_ids,
        }

        if not filters['participants']:
            return Response({'Error': 'This field is required.'}, status=400)
        if not participants_ids or len(participants_ids) < 2:
            return Response({'Error': 'At least 2 participants are required.'}, status=400)
        
        participants = User.objects.filter(pk__in=participants_ids)
        if len(participants) != len(participants_ids):
            return Response({'Error': 'Some or all users not exists'}, status=404)
        
        conversation = Conversation.objects.create(title=request.data.get('title'))
        conversation.participants.set(participants)
        dto = self.get_serializer(conversation).data

        return Response(dto, status=201)