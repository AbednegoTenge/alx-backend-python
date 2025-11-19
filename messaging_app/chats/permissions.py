from rest_framework import permissions


class IsMessageSenderOrParticipant(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):
        # Get the user from the request
        user = request.user
        # check if the user is the sender of the message or the recipient of the message
        if user == obj.sender or user in obj.conversation.participants.all():
            return True
        return False