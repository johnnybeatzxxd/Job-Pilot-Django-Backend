import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# Create your models here.

from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True) 
        extra_fields.setdefault('is_staff', False)  
        extra_fields.setdefault('is_superuser', False)  

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    company_name = models.CharField(max_length=40, blank=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    role = models.CharField(max_length=10, choices=[('candidate', 'Candidate'), ('recruiter', 'Recruiter')])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    is_superuser = models.BooleanField(default=False)  
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('candidate', 'Candidate'), ('recruiter', 'Recruiter')],default='candidate')
    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    email = models.EmailField()
    skills = models.JSONField(default=list,blank=True)
    bio = models.TextField()
    profile_image_url = models.URLField(blank=True)
    company_name = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_website = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    created_at = models.DateTimeField(default=models.functions.Now())
    updated_at = models.DateTimeField(auto_now=True)
