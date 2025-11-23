from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for User model"""
    list_display = ('user_id', 'email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('user_id', 'phone_number', 'role', 'created_at')
        }),
    )
    
    readonly_fields = ('user_id', 'created_at')


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin configuration for Conversation model"""
    list_display = ('conversation_id', 'get_participants', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('conversation_id',)
    filter_horizontal = ('participants',)
    readonly_fields = ('conversation_id', 'created_at')
    
    def get_participants(self, obj):
        """Display participant names"""
        return ', '.join([f"{p.first_name} {p.last_name}" for p in obj.participants.all()[:3]])
    get_participants.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin configuration for Message model"""
    list_display = ('message_id', 'sender', 'conversation', 'sent_at', 'get_message_preview')
    list_filter = ('sent_at', 'conversation')
    search_fields = ('message_body', 'sender__email', 'sender__first_name', 'sender__last_name')
    readonly_fields = ('message_id', 'sent_at')
    ordering = ('-sent_at',)
    
    def get_message_preview(self, obj):
        """Display first 50 characters of message"""
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body
    get_message_preview.short_description = 'Message Preview'
