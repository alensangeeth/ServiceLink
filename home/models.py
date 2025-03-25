from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    USER_ROLES = [
        ('customer', 'Customer'),
        ('provider', 'Provider'),
        ('admin', 'Admin'),
    ]

    user_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Ensure password is hashed!
    phone = models.CharField(max_length=10, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='customer')
    profile_pic = models.CharField(max_length=255, blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True, default=now)

    username = None  

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = ['full_name']  # Other fields required when creating a superuser

    class Meta:
        db_table = 'users'

    def set_password(self, raw_password):
        """Hashes the password before saving"""
        self.password = make_password(raw_password)

    def __str__(self):
        return self.full_name
    
# Category Model
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)  # Auto-incremented ID
    category_name = models.CharField(max_length=255, null=True, blank=True)  # Nullable field

    class Meta:
        db_table = "categories"

    def __str__(self):
        return self.category_name  # Fix: Use `category_name` instead of `name`


    
class ServiceProvider(models.Model):
    provider_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 
    phone = models.CharField(max_length=20)
    address = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=False)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'service_providers'  # Explicitly set the table name