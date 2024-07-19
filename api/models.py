from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.conf import settings
from rest_framework.authtoken.models import Token
from cloudinary.models import CloudinaryField

class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone_number, department, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        username = email  # Use email as username if needed
        
        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name,
                          phone_number=phone_number, department=department, role=role, **extra_fields)
        
        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, first_name, last_name, password=password, **extra_fields) 

class User(AbstractUser):
    profile_picture=CloudinaryField("image")
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("employee", "Employee"),
        ("superadmin", "SuperAdmin"),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='employee')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number', 'department', 'role']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Asset(models.Model):
    image=CloudinaryField('image')
    name=models.CharField(max_length=30)
    description=models.TextField()
    category=models.CharField(max_length=30)
    serial_number=models.CharField(max_length=100)
    tag=models.CharField(max_length=50)
    status=models.BooleanField(default=True)
    #created_at=models.DateTimeField(auto_now_add=True)
    asset_type=models.CharField(max_length=30)

class Request(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="requests")
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requests")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="pending")