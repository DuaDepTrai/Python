from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.students_list, name='students_list'),
    path('add/', views.add_student, name='add_student'),
    path('update/<int:id>', views.update_student, name='update_student'),
    path('delete/<int:id>', views.delete_student, name='delete_student'),
    
    path('api/students/', api_views.api_students_list, name='api_students_list'),
]