from django.urls import path
from users.views import user_list  # Import từ users
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("users/", user_list, name="user_list"),  # Thêm đường dẫn cho user list
]