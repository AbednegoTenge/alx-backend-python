from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from .models import Message
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth.models import User
from django.db.models import Q



# Create your views here.

def delete_user(request):
    if request.user.is_authenticated:
        user = request.user
        user.delete()

        logout(request)
        return redirect('home')
    return redirect('login')

@login_required
@cache_page(60, key_prefix='user_messages')
def get_messages(request, user_id):
    other_user = get_object_or_404(User, pk=user_id)
    user = request.user
    messages = Message.objects.filter(
        (Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user))
    ).order_by('timestamp')

    data = serializers.serialize('json', messages)
    return JsonResponse(data, safe=False)


@login_required
def unread_messages(request):
    user = request.user
    unread_messages = Message.unread.unread_for_user(user).only('id', 'sender', 'content', 'timestamp').order_by('-timestamp')
    data = serializers.serialize('json', unread_messages)
    return JsonResponse(data, safe=False)



    
        
