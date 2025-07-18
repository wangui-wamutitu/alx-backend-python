from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve and create conversations
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return conversations the current user is part of
        return Conversation.objects.filter(participants=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return ConversationSerializer

    def perform_create(self, serializer):
        # Automatically set the current user as participant_a
        serializer.save(participant_a=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, and create messages in conversations
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def get_serializer_class(self):
        if self.action == "create":
            return MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
