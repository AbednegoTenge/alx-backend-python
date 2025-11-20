from rest_framework import viewsets, filters
from django.db.models import Q
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from .permissions import IsMessageSenderOrParticipant, IsParticipantOfConversation
from rest_framework.permissions import IsAuthenticated
from .auth import CustomTokenAuthentication
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'message_id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    permission_classes = [IsAuthenticated, IsMessageSenderOrParticipant]
    authentication_classes = [CustomTokenAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(sender=user) | Q(conversation__participants=user)
        ).distinct()

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    lookup_field = 'conversation_id'
    search_fields = ['participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    authentication_classes = [CustomTokenAuthentication]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(participants=user)

