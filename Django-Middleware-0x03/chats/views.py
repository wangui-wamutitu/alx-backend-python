from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsOwnerOrReadOnly, IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import StandardResultsSetPagination
from chats.models import User


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
        serializer.save(participants=[self.request.user])


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet to list, retrieve, and create messages in user's conversations.
    """

    permission_classes = [IsAuthenticated & IsParticipantOfConversation]
    serializer_class = MessageSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation"]
    filterset_class = MessageFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation_id")
        recipient_id = self.request.data.get("recipient_id")

        if not conversation_id or not recipient_id:
            raise PermissionDenied("conversation_id and recipient_id are required.")

        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise PermissionDenied("Conversation not found.")

        try:
            recipient = User.objects.get(user_id=recipient_id)
        except User.DoesNotExist:
            raise PermissionDenied("Recipient not found.")

        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")
        if recipient not in conversation.participants.all():
            raise PermissionDenied("Recipient is not a participant in this conversation.")

        serializer.save(
            sender=self.request.user,
            recipient=recipient,
            conversation=conversation,
        )
