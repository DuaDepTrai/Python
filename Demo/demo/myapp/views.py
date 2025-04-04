from django.shortcuts import render, HttpResponse, redirect
# from django_redis import get_redis_connection
from users.models import User
from .decorators import login_required_custom

# Create your views here.
@login_required_custom
def home(request):
    return render(request, 'home.html')