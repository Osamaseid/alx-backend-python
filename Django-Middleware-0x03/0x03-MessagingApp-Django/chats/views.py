from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .permissions import IsConversationParticipant, IsMessageParticipant

class ConversationViewSet(viewsets.ModelViewSet):
   serializer_class = ConversationSerializer
   filter_backends = [filters.OrderingFilter]
   ordering_fields = ['created_at']
   permission_classes = (IsConversationParticipant,)

   def get_queryset(self):
       return Conversation.objects.filter(participants=self.request.user)

   def create(self, request):
       serializer = self.get_serializer(data=request.data)
       serializer.is_valid(raise_exception=True)
       conversation = serializer.save()
       conversation.participants.add(self.request.user)
       return Response(serializer.data, status=status.HTTP_201_CREATED)

   def retrieve(self, request, pk=None):
       conversation = self.get_object()
       if request.user not in conversation.participants.all():
           return Response(status=status.HTTP_403_FORBIDDEN)
       serializer = self.get_serializer(conversation)
       return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
   serializer_class = MessageSerializer
   filter_backends = [filters.OrderingFilter]
   ordering_fields = ['sent_at']
   permission_classes = (IsMessageParticipant,)

   def get_queryset(self):
       return Message.objects.filter(conversation__participants=self.request.user)

   def create(self, request):
       serializer = self.get_serializer(data=request.data) 
       serializer.is_valid(raise_exception=True)
       serializer.save(sender=self.request.user)
       return Response(serializer.data, status=status.HTTP_201_CREATED)
class MessageViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    
