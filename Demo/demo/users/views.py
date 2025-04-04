from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
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
import hashlib
import uuid, json
import logging

# Create your views here.
logger = logging.getLogger('users')  # Đặt tên logger trùng với settings.py

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Không lưu ngay vào DB
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()  # Lưu vào DB
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

# @login_required_custom
def user_list(request):
    # xử lý show user list
    return render(request, 'user_list.html', {'users': User.objects.all()})

def update_user(request, id):
    user = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)

            # Nếu password có thay đổi, hash lại
            raw_password = form.cleaned_data.get('password')
            if raw_password:
                user.set_password(raw_password)

            user.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)

    return render(request, 'update_user.html', {'form': form, 'user': user})


def delete_user(request, id):  # Nhận tham số id
    user = get_object_or_404(User, id=id)  # Lấy người dùng theo id
    if request.method == 'POST':  # Nếu là POST, xóa người dùng
        user.delete()
        return redirect('user_list')  # Chuyển đến trang danh sách người dùng
    return render(request, 'confirm_delete.html', {'user': user})  # Nếu là GET, hiển thị form xác nhận

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Kiểm tra user có tồn tại không
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            # Nếu user tồn tại, kiểm tra mật khẩu
            if user is not None:
                # Kiểm tra mật khẩu bằng check_password
                if check_password(password, user.password):
                    login(request, user)  # Đăng nhập với Django
                    return redirect('user_list')
                else:
                    messages.error(request, 'Invalid password')  # Mật khẩu sai
                    return redirect('login')
            else:
                messages.error(request, 'Invalid username')  # Tên người dùng không tồn tại
                return redirect('login')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# def user_list(request):
#     session_id = request.COOKIES.get('sessionID')
#     if not session_id:
#         return redirect('login')
#     redis_conn = get_redis_connection("default")
#     session_data = redis_conn.get(session_id)
    
#     if not session_data:
#         return redirect('login')
    
#     return render(request, 'user_list.html', {'users': User.objects.all()})

# def login_user(request):
#     logger.debug("Login view accessed.")  # Log truy cập login

#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']

#             try:
#                 user = User.objects.get(username=username)
#             except User.DoesNotExist:
#                 messages.error(request, "User not found")
#                 logger.warning(f"Login failed: User {username} not found")
#                 return redirect('login')

#             if user.check_password(password):
#                 logger.info(f"User {user.username} logged in successfully")

#                 request.session.create()
#                 user_data = {
#                     'sessionID': request.session.session_key,
#                     'username': user.username,
#                     'email': user.email,
#                     'phone': user.phone,
#                 }

#                 redis_conn = get_redis_connection("default")
#                 redis_conn.set(request.session.session_key, str(user_data), ex=3600)

#                 response = redirect('/')
#                 response.set_cookie('sessionID', request.session.session_key, max_age=3600)
#                 return response
#             else:
#                 messages.error(request, "Invalid password")
#                 logger.warning(f"Login failed: Wrong password for {username}")
#                 return redirect('login')  # <== bạn thiếu redirect ở đây
#     else:
#         form = LoginForm()

#     return render(request, 'login.html', {'form': form})

# def check_session(request):
#     session_id = request.COOKIES.get('sessionID')
#     if session_id:
#         redis_conn = get_redis_connection("default")
#         user_data = redis_conn.get(session_id)
#         if user_data:
#             return redirect('home')
#     return redirect('login')


# users/views.py


# def login_view(request):
#     error = ''
#     if request.method == 'POST':
#         identity = request.POST.get('identity')
#         password = request.POST.get('password')
        
#         try:
#             user = User.objects.get(Q(username=identity) | Q(email=identity) | Q(phone=identity))
#             if user.check_password(password):
#                 session_id = str(uuid.uuid4())
#                 redis_conn = get_redis_connection("default")
#                 session_data = {
#                     'username': user.username,
#                     'email': user.email,
#                     'phone': user.phone,
#                 }
#                 redis_conn.set(session_id, json.dumps(session_data), ex=86400)

#                 response = redirect('user_list')
#                 response.set_cookie('sessionid', session_id)

#                 return response
#             else:
#                 error = 'Sai mật khẩu!'
#         except User.DoesNotExist:
#             error = 'Không tìm thấy tài khoản.'

#     return render(request, 'login.html', {'error': error})