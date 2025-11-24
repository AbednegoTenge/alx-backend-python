from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Message, Notification
from django.core.mail import send_mail



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

