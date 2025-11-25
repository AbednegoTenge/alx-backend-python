from nt import times
from django.db import models
from django.contrib.auth.models import User


# Custom Manager
class UnreadMessagesManager(models.Manager):

    def unread(self, user):
        return self.filter(is_read=False, receiver=user).only('id', 'sender', 'content', 'timestamp')

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_messages')
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    unread_messages = UnreadMessagesManager()


    def __str__(self):
        return f'{self.sender} to {self.recipient}: {self.content}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.message.content}'


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_history')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_history')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=False)




