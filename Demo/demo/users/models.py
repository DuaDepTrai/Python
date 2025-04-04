from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, fullname, phone, email, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, fullname=fullname, phone=phone, email=email)
        user.set_password(password)  # Đảm bảo mật khẩu được hash
        user.save(using=self._db)
        return user

    def create_superuser(self, username, fullname, phone, email, password=None):
        user = self.create_user(username, fullname, phone, email, password)
        user.is_admin = True  # Cần có cờ này nếu tạo admin
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
