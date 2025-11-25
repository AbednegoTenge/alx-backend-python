from django.urls import path
from . import views

urlpatterns = [
    path('delete_user/', views.delete_user, name='delete_user'),
    path('messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('inbox/', views.unread_messages, name='unread_messages')
]