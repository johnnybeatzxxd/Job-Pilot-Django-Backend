from django.db import models
from users.models import *
import uuid
# Create your models here.

class Job(models.Model):
    job_id = models.CharField(max_length=8, default=uuid.uuid4().hex[:8], editable=False, unique=True)
    company = models.ForeignKey(Profile, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    salary_type = models.CharField(choices=[('fixed', 'Fixed'), ('hourly', 'Hourly')])
    job_type = models.CharField(choices=[('remote', 'Remote'), ('on-site', 'On-site'), ('hybrid', 'Hybrid')])
    level = models.CharField(choices=[('entry', 'Entry'), ('intermediate', 'Intermediate'), ('senior', 'Senior'), ('lead', 'Lead'), ('expert', 'Expert')])
    maximum_applications = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=15,decimal_places=2)
    estimated_budget = models.DecimalField(max_digits=15,decimal_places=2)
    description = models.TextField()
    requirements = models.JSONField(default=list)
    desirable_skills = models.JSONField(default=list,null=True)
    tags = models.JSONField(default=list)
