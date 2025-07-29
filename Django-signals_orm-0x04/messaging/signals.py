from django.dispatch import receiver
from .models import Message, Notification, MessageHistory, User
from django.db.models.signals import post_save, pre_save, post_delete
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
            message=instance,
            old_content=old_instance.content,
            edited_at=timezone.now(),
            edited_by=instance.sender,
        )


@receiver(post_delete, sender=User)
def delete_related_user_info(sender, instance, **kwargs):
    # Delete messages
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications
    Notification.objects.filter(user=instance).delete()

    # Delete message histories
    histories = MessageHistory.objects.filter(
        messages__sender=instance
    ) | MessageHistory.objects.filter(messages__receiver=instance)
    histories.distinct().delete()
