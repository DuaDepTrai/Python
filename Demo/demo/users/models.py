from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, fullname, phone, email, password=None):
        if not username:
            raise ValueError('The Username field must be set')
        if not fullname:
            raise ValueError('The Fullname field must be set')
        if not phone:
            raise ValueError('The Phone field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')
        email = self.normalize_email(email)
        user = self.model(
            username=username, 
            fullname=fullname, 
            phone=phone, 
            email=email)
        user.set_password(password)  # Đảm bảo mật khẩu được hash
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    fullname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'fullname', 'phone']  # Các trường bắt buộc khác

    objects = UserManager()

    def __str__(self):
        return self.username