from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.db.utils import IntegrityError
import json
from users.models import User, Profile
from jobs.models import Job
from applications.models import Application
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

@login_required
@api_view(['POST'])
def submit(request):
    user = request.user
    job_id = request.data.get("jobId")
    application = request.data.get("application")
    resume = request.data.get("resume")
    job = Job.objects.get(job_id=job_id)
    applied_user = Profile.objects.get(email=user.email)
    company = job.company
    country = applied_user.country
    job_title = job.job_title
    job_salary = job.salary

    try:
        application = Application.objects.create(
            job=job,
            applied_user=applied_user,
            company=company,
            job_title = job_title,
            country=country,
            job_salary=job_salary,
            application = application,
            resume= resume,
        )
        applied_user.applied_jobs.append(application.app_id)
        applied_user.save()
        return JsonResponse({"message":"Your application submitted successfuly."})    
    except:
        return JsonResponse({"error":"User or Job not found."},status=400)
    
