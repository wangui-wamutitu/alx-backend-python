from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone
from django.conf import settings


class User(AbstractUser):
    """
    Custom user model extending AbstractUser.
    Replaces id with UUID and adds role, phone number, etc.
    """

    class Roles(models.TextChoices):
        GUEST = "guest", "Guest"
        HOST = "host", "Host"
        ADMIN = "admin", "Admin"

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    email = models.EmailField(unique=True, null=False, blank=False, db_index=True)
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    password_hash = models.CharField(max_length=128, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.GUEST)
    created_at = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"  # use email for login
    REQUIRED_FIELDS = ["first_name", "last_name", "username"]


def __str__(self):
    return f"{self.email} ({self.role})"


class Conversation(models.Model):
    """
    Tracks which users are involved in a conversation.
    """

    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    participants = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="conversations_as_a"
    )

    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["participant_a", "participant_b"],
                name="unique_conversation_pair",
            )
        ]

    def __str__(self):
        return f"Conversation between {self.participant_a.email} and {self.participant_b.email}"


class Message(models.Model):
    """
    Message model containing the sender, conversation
    Contains the actual messages, linked to sender and conversation.
    """

    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True, db_index=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages_sent"
    )

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="messages_received",
    )

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    message_body = models.CharField(max_length=200, null=False, blank=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"From {self.sender.email} to {self.recipient.email} @ {self.sent_at}"
