from django.db import models


# Custom Manager
class UnreadMessagesManager(models.Manager):

    def unread_for_user(self, user):
        return self.filter(is_read=False, receiver=user)