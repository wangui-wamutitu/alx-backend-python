from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings
from django.utils import timezone
from .managers import UnreadMessagesManager


class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, db_index=True
    )
    username = models.TextField(max_length=150, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"{self.username} has been created on {self.created_at}"


class Message(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, db_index=True
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="message_sent"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="message_received",
    )
    content = models.TextField(max_length=250, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="replies")
    read = models.BooleanField(default=True)

    unread = UnreadMessagesManager()

def __str__(self):
    return f"{self.sender} sent a message to {self.receiver}"


class Notification(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, unique=True, db_index=True
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="related_message",
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )

    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"Notification sent to {self.sent_to} about {self.message}"


class MessageHistory(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, db_index=True)
    message = models.ForeignKey('Message', on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="message_editor")


def __str__(self):
    return f"Edited by {self.edited_by} on {self.edited_at}"
