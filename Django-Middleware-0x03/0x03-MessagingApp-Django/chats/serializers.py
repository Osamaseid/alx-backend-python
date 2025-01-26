from rest_framework import serializers
from .models import Conversation, CustomUser, Message

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    participants = CustomUserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    default_message = serializers.CharField(default="Initiate for endless conversation", read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'

    def get_participant_count(self, obj):
        return obj.participants.count()

    def validate(self, obj):
        if not obj.participants.exists():
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return obj