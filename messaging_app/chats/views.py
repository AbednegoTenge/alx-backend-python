from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user_id'


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation model with list and create operations"""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    lookup_field = 'conversation_id'
    
    def list(self, request):
        """List all conversations"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, conversation_id=None):
        """Retrieve a specific conversation"""
        conversation = get_object_or_404(self.queryset, conversation_id=conversation_id)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data)
    
    def create(self, request):
        """Create a new conversation"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()
        return Response(
            self.get_serializer(conversation).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'], url_path='send-message')
    def send_message(self, request, conversation_id=None):
        """Send a message to an existing conversation"""
        conversation = get_object_or_404(self.queryset, conversation_id=conversation_id)
        
        # Add conversation_id to the request data
        message_data = request.data.copy()
        message_data['conversation_id'] = conversation_id
        
        # If sender_id is not provided, use the authenticated user
        if 'sender_id' not in message_data and request.user.is_authenticated:
            message_data['sender_id'] = request.user.user_id
        
        serializer = MessageSerializer(data=message_data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        
        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['get'], url_path='messages')
    def list_messages(self, request, conversation_id=None):
        """List all messages in a conversation"""
        conversation = get_object_or_404(self.queryset, conversation_id=conversation_id)
        messages = conversation.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Message model with list and create operations"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    lookup_field = 'message_id'
    
    def list(self, request):
        """List all messages"""
        queryset = self.get_queryset()
        
        # Filter by conversation if conversation_id is provided
        conversation_id = request.query_params.get('conversation_id', None)
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, message_id=None):
        """Retrieve a specific message"""
        message = get_object_or_404(self.queryset, message_id=message_id)
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    def create(self, request):
        """Create a new message (send message to a conversation)"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response(
            self.get_serializer(message).data,
            status=status.HTTP_201_CREATED
        )
