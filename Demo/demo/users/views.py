from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from django_redis import get_redis_connection
from django.urls import reverse
from .forms import LoginForm
from .forms import UserForm
from .models import User
from .decorators import login_required_custom

# Create your views here.

@login_required_custom
def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])  
            user.save()  #
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

@login_required_custom
def user_list(request):
    return render(request, 'user_list.html', {'users': User.objects.all()})

@login_required_custom
def update_user(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            re_password = form.cleaned_data.get('re_password')
            
            if password and password != re_password:
                form.add_error('re_password', "Passwords do not match")
            else:
                user = form.save(commit=False)
                if password:
                    user.set_password(password)
                user.save()
                return redirect('user_list')
    else:
        form = UserForm(instance=user)

    return render(request, 'update_user.html', {'form': form, 'user': user})

@login_required_custom
def delete_user(request, id):
    user = get_object_or_404(User, id=id) 
    if request.method == 'POST':  
        user.delete()
        return redirect('user_list')  
    return render(request, 'confirm_delete.html', {'user': user})  

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user) 
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required_custom
def logout_view(request):
    return redirect('confirm_logout')

@login_required_custom
def confirm_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')
    return render(request, 'confirm_logout.html')        