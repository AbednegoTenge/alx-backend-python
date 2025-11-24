from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, post_delete
from .models import Message, Notification, MessageHistory
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User





@receiver(post_save, sender=Message)
def send_message_notification(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'New Message',
            f'You have a new message from {instance.sender.username}: {instance.content}',
            'admin@django.com',
            [instance.receiver.email],
            fail_silently=True
        )
        Notification.objects.create(user=instance.receiver, message=instance)
        Notification.objects.create(user=instance.sender, message=instance)


@receiver(pre_save, sender=Message)
def update_message_history(sender, instance, **kwargs):
    if instance.pk:
        old_message = Message.objects.get(pk=instance.pk)
        if old_message.content != instance.content:
            MessageHistory.objects.create(
                message=instance, 
                sender=instance.sender, 
                receiver=instance.receiver, 
                content=old_message.content,
                timestamp=old_message.timestamp
            )
            instance.edited = True
            instance.edited_at = timezone.now()
            instance.edited_by = instance.sender


@receiver(post_delete, sender=User)
def delete_message_history(sender, instance, **kwargs):

    #Get message sent or received by user
    user_messages = Message.objects.filter(sender=instance.sender) | Message.objects.filter(receiver=instance.receiver)
    # Delete message history for those messages
    MessageHistory.objects.filter(message__in=user_messages).delete()
    # Delete notifications for those messages
    Notification.objects.filter(user=instance).delete()
    # Delete notifications tied to the message
    Notification.objects.filter(message__in=user_messages).delete()
    # Delete the messages themselves
    user_messages.delete()