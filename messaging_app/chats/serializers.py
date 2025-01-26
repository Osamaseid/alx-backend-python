from .models import User, Conversation, Message
from rest_framework import serializers
from django.utils.timezone import now

class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="user-detail")
    member_since = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['url', 'user_id', 'full_name', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'member_since', 'created_at']
        read_only_fields = ['user_id', 'member_since', 'created_at']

    def get_member_since(self, obj):
        return (now() - obj.created_at).days
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def validate_email(self, value):
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_phone_number(self, value):
        allowed_chars = ['+', ' ', '(', ')', '-']
        if value and all([char.isdigit() or char in allowed_chars for char in value]):
            raise serializers.ValidationError("Phone number can only contain digits.")


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="message-detail")
    sender = UserSerializer()
    conversation_title = serializers.CharField(source='conversation.title', read_only=True)
    sent_since = serializers.SerializerMethodField()
    read_since = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['url', 'message_id', 'message_body', 'sender', 'conversation_title', 'sent_at', 'read_at', 'sent_since', 'read_since']
        read_only_fields = ['message_id', 'sent_at', 'read_at', 'sent_since', 'read_since']

    def get_sent_since(self, obj):
        return (now() - obj.sent_at).seconds
    
    def get_read_since(self, obj):
        if obj.read_at:
            return (obj.read_at - obj.sent_at).seconds
        return None
    
    def validate_message_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        if len(value) > 500:
            raise serializers.ValidationError("Message body is too long.")
        return value

class ConversationSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="conversation-detail")
    participants = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)
    created_since = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['url', 'conversation_id', 'title', 'participants', 'created_since', 'created_at', 'messages']
        read_only_fields = ['conversation_id', 'created_since', 'created_at', 'messages']
    
    def get_participants(self, obj):
        participants = obj.participants.all()
        context = self.context
        return UserSerializer(participants, many=True, context=context).data

    def get_created_since(self, obj):
        return (now() - obj.created_at).days

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title can't be empty.")
        if len(value) > 255:
            raise serializers.ValidationError("Title is too long.")
        return value
    
    def validate(self, data):
        if 'participants' in self.initial_data and len(self.initial_data['participants']) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return data

    def create(self, validated_data):
        participants_data = self.initial_data.pop('participants', [])
        conversation = Conversation.objects.create(**validated_data)
        for participant_data in participants_data:
            user = User.objects.get(user_id=participant_data['user_id'])
            conversation.participants.add(user)
        return conversation

class NestedUserSerializer(serializers.ModelSerializer):
    """For POST requests where only `user_id` is needed."""
    class Meta:
        model = User
        fields = ['user_id']