from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.db.utils import IntegrityError
import json
from users.models import Profile, User
from jobs.models import Job
from applications.models import Application
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
@api_view(['GET'])
def get_overview(request):
    try:
        user = request.user
        user_profile = Profile.objects.select_related('user').get(email=user.email)
        user_app_ids = user_profile.applied_jobs
        favorite_jobs_ids = user_profile.favorite_jobs
        applied_jobs_number = len(user_app_ids)
        favorite_jobs_number = len(favorite_jobs_ids)
        
        recently_applied = []
        applications = Application.objects.select_related('company', 'job')\
            .filter(app_id__in=user_app_ids[-3:])\
            .order_by('-created_at')

        for application in applications:
            recently_applied.append({
                "company_name": application.company.company_name,
                "applied_date": application.created_at,
                "profile_picture": application.company.profile_image_url,
                "country": application.job.country,
                "salary": application.job_salary,
                "salary_type": application.job.salary_type
            })

        overview = {
            "applied_nums": applied_jobs_number,
            "favorite_nums": favorite_jobs_number,
            "alert": 0,
            "recently_applied": recently_applied
        }
        return JsonResponse({"message":overview})
        
    except Profile.DoesNotExist:
        return JsonResponse({"error": "User profile not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@api_view(['GET'])
def get_applied_jobs(request):
    pass

@login_required
@api_view(['GET'])
def get_favorite_jobs(request):
    pass