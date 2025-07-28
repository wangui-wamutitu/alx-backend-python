from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.db.models.signals import post_save, pre_save
from django.utils import timezone


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)


@receiver(pre_save, sender=Message)
def log_edit_message(sender, instance, **kwargs):
    if instance.edited:
        Message.objects.update(edited=True)
        MessageHistory.object.update(messages=instance)

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        # It's a new message, not an edit
        return

    if old_instance.content != instance.content:
        instance.edited = True
        instance.edited_at = timezone.now()

        # Log old content to history
        MessageHistory.objects.create(
            message=instance, old_content=old_instance.content, edited_at=timezone.now()
        )
