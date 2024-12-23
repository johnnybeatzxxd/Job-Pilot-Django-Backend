from django.db import models
from jobs.models import *
from users.models import *
import uuid
# Create your models here.

def generate_app_id():
    return uuid.uuid4().hex[:8] 


class Application(models.Model):
    app_id = models.CharField(max_length=8, default=generate_app_id, editable=False, unique=True)
    job = models.OneToOneField(Job, on_delete=models.CASCADE)
    applied_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='applications_applied')
    company = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='applications_company')
    job_title = models.CharField(max_length=100)
    country = models.CharField(max_length=100,blank=True)
    job_salary = models.DecimalField(max_digits=15,decimal_places=2)
    application = models.TextField()
    resume = models.CharField(max_length=1000,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
