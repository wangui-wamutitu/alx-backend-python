from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Message


User = get_user_model()

def build_thread(message):
    return {
        "id": str(message.id),
        "sender": message.sender.username,
        "receiver": message.receiver.username,
        "content": message.content,
        "created_at": message.created_at,
        "replies": [build_thread(reply) for reply in message.replies.all()]
    }


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="threads")
    def get_threaded_messages(self, request):

        top_level_messages = (
            Message.objects.filter(
                parent_message__isnull=True,
                sender=request.user 
            )
            .select_related("sender", "receiver") 
            .prefetch_related(
                "replies",                # Prefetch direct replies
                "replies__sender",        # Prefetch sender of replies
                "replies__receiver",      # Prefetch receiver of replies
                "replies__replies",       # Prefetch second-level replies
            )
        )

        threads = [build_thread(msg) for msg in top_level_messages]
        return Response(threads, status=status.HTTP_200_OK)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    # DELETE /users/delete-account/
    @action(detail=False, methods=["delete"], url_path="delete-account")
    def delete_user(self, request):
        user = request.user
        user.delete()
        return Response(
            {"detail": "Your account has been deleted"},
            status=status.HTTP_204_NO_CONTENT,
        )

   