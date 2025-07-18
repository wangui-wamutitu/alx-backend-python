from .models import User, Message, Conversation
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Includes all fields, handles UUID primary key, and formats nested choices.
    """
    role = serializers.ChoiceField(choices=User.Roles.choices)

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "first_name",
            "last_name",
            "password_hash",
            "phone_number",
            "role",
            "created_at",
        ]
        read_only_fields = ["user_id", "created_at"]
        last_name = serializers.CharField(read_only=True, default="doe")

class UserMiniSerializer(serializers.ModelSerializer):
    """
    Serializer to be used
    """
    class Meta:
        model = User
        fields = ["user_id", "email", "first_name", "last_name", "role"]
        read_only_fields = fields

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserMiniSerializer(read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "created_at",
        ]
        read_only_fields = fields

    def get_messages(self, obj):
        from .serializers import MessageSerializer
        return MessageSerializer(obj.messages.all(), many=True).data

class MessageSerializer(serializers.ModelSerializer):
    sender = UserMiniSerializer(read_only=True)
    recipient = UserMiniSerializer(read_only=True)
    conversation = ConversationSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "sender",
            "recipient",
            "conversation",
            "message_body",
            "sent_at",
        ]
        read_only_fields = ["message_id", "sent_at"]

    def validate(self, data):
        if data["sender"] == data["recipient"]:
            raise serializers.ValidationError("Sender and recipient cannot be the same.")
        return data
