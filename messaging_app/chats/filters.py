import django_filters
from .models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

class MessageFilter(django_filters.FilterSet):
    # filter message by sender
    sender = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    # filter message by conversation
    conversation_participant = django_filters.ModelMultipleChoiceFilter(
        field_name='conversation__participants',
        queryset=User.objects.all(),
        to_field_name='user_id'
    )
    # filter message by date range
    start_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['sender', 'conversation_participant', 'start_date', 'end_date']