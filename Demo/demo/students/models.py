from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

class Student(models.Model):
    studentID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    className = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=200)
    math = models.DecimalField(max_digits=5, decimal_places=2)
    physics = models.DecimalField(max_digits=5, decimal_places=2)
    chemistry = models.DecimalField(max_digits=5, decimal_places=2)
    avg = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        self.avg = (self.math + self.physics + self.chemistry)/3
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name