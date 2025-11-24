from django.shortcuts import render, redirect
from django.contrib.auth import logout


# Create your views here.

def delete_user(request):
    if request.user.is_authenticated:
        user = request.user
        user.delete()

        logout(request)
        return redirect('home')
    return redirect('login')

    
        
