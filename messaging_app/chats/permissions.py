from rest_framework import permissions


class IsMessageSenderOrParticipant(permissions.BasePermission):
    """
    Permission class to check if user is the sender of a message or a participant in the conversation.
    - Participants can view messages (GET)
    - Only the sender can modify/delete messages (PUT, PATCH, DELETE)
    """
    
    def has_object_permission(self, request, view, obj):
        # Get the user from the request
        user = request.user
        
        # Check if user is authenticated
        if not user or not user.is_authenticated:
            return False
        
        # Check if user is a participant in the conversation
        # Use filter().exists() for better performance
        is_participant = obj.conversation.participants.filter(user_id=user.user_id).exists()
        if not is_participant:
            return False
        
        # For safe methods (GET, HEAD, OPTIONS), participants can view
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # For write methods (PUT, PATCH, DELETE), only sender can modify/delete
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return user.user_id == obj.sender.user_id
        
        # For other methods (POST), participant can create (handled by view)
        return True


class IsParticipantOfConversation(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        # Get the user from the request
        user = request.user
        # check if the user is a participant of the conversation
        # if the obj is a conversation
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        # if the obj is participant
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        return False