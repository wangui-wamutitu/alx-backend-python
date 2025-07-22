from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly, IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, and create conversations for the authenticated user.
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = ConversationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["participants"]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(participant_a=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, and create messages in user's conversations.
    """

    permission_classes = [IsAuthenticated & IsParticipantOfConversation]
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation"]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated & IsParticipantOfConversation]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation_id")
        if not conversation_id:
            raise PermissionDenied("conversation_id is required.")

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        if self.request.user not in conversation.participants.all():
            from rest_framework.status import HTTP_403_FORBIDDEN
            raise PermissionDenied(detail="You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)