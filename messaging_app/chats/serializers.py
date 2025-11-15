from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    user_id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    password_hash = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'role',
            'password',
            'password_hash',
            'created_at',
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def create(self, validated_data):
        """Create user with password hashing"""
        password = validated_data.pop('password', None)
        
        # Validate password is provided before creating user
        if not password:
            raise serializers.ValidationError({'password': 'Password is required'})
        
        # Create user first
        user = User.objects.create(**validated_data)
        # Then set and hash the password
        user.set_password(password)
        user.password_hash = user.password  # Store the hashed password
        user.save()
        
        return user
    
    def update(self, instance, validated_data):
        """Update user with password hashing if password is provided"""
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
            instance.password_hash = instance.password  # Store the hashed password
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model with nested sender information"""
    message_id = serializers.UUIDField(read_only=True)
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=True)
    conversation_id = serializers.UUIDField(write_only=True, required=True)
    sent_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_id',
            'conversation_id',
            'message_body',
            'sent_at',
        ]
        extra_kwargs = {
            'message_body': {'required': True},
        }
    
    def create(self, validated_data):
        """Create message with sender and conversation"""
        sender_id = validated_data.pop('sender_id')
        conversation_id = validated_data.pop('conversation_id')
        
        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            raise serializers.ValidationError({'sender_id': 'User does not exist'})
        
        try:
            conversation = Conversation.objects.get(conversation_id=conversation_id)
        except Conversation.DoesNotExist:
            raise serializers.ValidationError({'conversation_id': 'Conversation does not exist'})
        
        return Message.objects.create(
            sender=sender,
            conversation=conversation,
            **validated_data
        )


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested participants and messages"""
    conversation_id = serializers.UUIDField(read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    messages = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participant_ids',
            'messages',
            'created_at',
        ]
    
    def get_messages(self, obj):
        """Get messages within the conversation using SerializerMethodField"""
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data
    
    def create(self, validated_data):
        """Create conversation with participants (many-to-many relationship)"""
        participant_ids = validated_data.pop('participant_ids')
        
        if not participant_ids:
            raise serializers.ValidationError({'participant_ids': 'At least one participant is required'})
        
        conversation = Conversation.objects.create()
        
        # Add participants (many-to-many)
        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            found_ids = set(participants.values_list('user_id', flat=True))
            missing_ids = set(participant_ids) - found_ids
            raise serializers.ValidationError({
                'participant_ids': f'Users with IDs {list(missing_ids)} do not exist'
            })
        
        conversation.participants.set(participants)
        return conversation
    
    def update(self, instance, validated_data):
        """Update conversation participants"""
        participant_ids = validated_data.pop('participant_ids', None)
        
        if participant_ids is not None:
            if not participant_ids:
                raise serializers.ValidationError({'participant_ids': 'At least one participant is required'})
            
            participants = User.objects.filter(user_id__in=participant_ids)
            if participants.count() != len(participant_ids):
                found_ids = set(participants.values_list('user_id', flat=True))
                missing_ids = set(participant_ids) - found_ids
                raise serializers.ValidationError({
                    'participant_ids': f'Users with IDs {list(missing_ids)} do not exist'
                })
            
            instance.participants.set(participants)
        
        return instance

