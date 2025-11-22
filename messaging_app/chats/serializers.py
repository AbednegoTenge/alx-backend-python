from rest_framework import serializers
from .models import Conversation, Message, User


class UserSerializer(serializers.ModelSerializer):
    # Fields that are read only
    user_id = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    # Field that is write only
    password = serializers.CharField(write_only=True, required=True)

    # Meta class for the serializer
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'password', 'phone_number', 'role', 'created_at']
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def create(self, validated_data):
        # Remove password from validated_data if it is provided
        password = validated_data.pop('password')
        if not password:
            raise serializers.ValidationError("Password is required")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.password_hash = user.password
        user.save()
        return user

    def update(self, instance, validated_data):
        # Remove password from validated_data if it is provided
        password = validated_data.pop('password', None)

        # Update the other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if password:
            instance.set_password(password)
            instance.password_hash = instance.password
        instance.save()
        return instance


    
class MessageSerializer(serializers.ModelSerializer):
    message_id = serializers.UUIDField(read_only=True)
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=True)
    conversation_id = serializers.UUIDField(write_only=True, required=True)
    message_body = serializers.CharField(write_only=False, required=True)
    sent_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'conversation_id', 'message_body', 'sent_at']
        extra_kwargs = {
            'sender_id': {'required': True},
            'conversation_id': {'required': True},
            'message_body': {'required': True},
        }

    def create(self, validated_data):
        # Get the sender and conversation objects
        sender_id = validated_data.pop('sender_id')
        conversation_id = validated_data.pop('conversation_id')

        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Sender not found")
        
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError("Conversation not found")
        
        # Create the message
        message = Message.objects.create(sender=sender, conversation=conversation, **validated_data)
        message.save()
        return message
        
    def update(self, instance, validated_data):
        # Update the other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Save the instance
        instance.save()
        return instance

class ConversationSerializer(serializers.ModelSerializer):
    conversation_id = serializers.UUIDField(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    participants_id = serializers.ListField(child=serializers.UUIDField(), write_only=True, required=True)
    messages = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participants_id', 'messages', 'created_at']
        extra_kwargs = {
            'participants_id': {'required': True},
        }

    def create(self, validated_data):
        participants_id = validated_data.pop('participants_id', None)
        
        if not participants_id:
            raise serializers.ValidationError("Participants are required")

        conversation = Conversation.objects.create()
        
        participants = User.objects.filter(user_id__in=participants_id)
        if participants.count() != len(participants_id):
            found_ids = set(participants.values_list('user_id', flat=True))
            missing_ids = set(participants_id) - found_ids
            raise serializers.ValidationError(f"Participants not found: {missing_ids}")
        
        conversation.participants.set(participants)
        return conversation

    def get_messages(self, obj):
        messages = obj.messages.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data

    def update(self, instance, validated_data):
        instance.message_body = validated_data.get('message_body', instance.message_body)
        instance.save()
        return instance 
    