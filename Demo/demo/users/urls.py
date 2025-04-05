from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    # path('', views.home, name='home'),
    path('add/', views.add_user, name='add_user'),
    path('update/<int:id>', views.update_user, name='update_user'),
    path('delete/<int:id>/', views.delete_user, name='delete_user'),  # Đảm bảo có <int:id> trong URL
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logout/confirm/', views.confirm_logout, name='confirm_logout')
    # path('home/', views.check_session, name='check_session'),
]