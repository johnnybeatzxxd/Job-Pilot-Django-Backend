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
        
        if user.role == 'recruiter':
            applications = Application.objects.select_related('applied_user', 'job')\
                .filter(company=user_profile)\
                .order_by('-created_at')[:3]

            recently_applied = []
            for application in applications:
                recently_applied.append({
                    "applicant_name": application.applied_user.full_name,
                    "applicant_title": application.applied_user.title,
                    "profile_picture": application.applied_user.profile_image_url,
                    "job_title": application.job.job_title,
                    "applied_date": application.created_at,
                    "status": "New"
                })

            overview = {
                "total_applications": Application.objects.filter(company=user_profile).count(),
                "active_jobs": Job.objects.filter(company=user_profile).count(),
                "total_views": 0,  
                "recently_applied": recently_applied
            }
        else:
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
                    "salary": application.job.salary,
                    "salary_type": application.job.salary_type
                })

            overview = {
                "applied_nums": applied_jobs_number,
                "favorite_nums": favorite_jobs_number,
                "alert": 0,
                "recently_applied": recently_applied
            }

        return JsonResponse({"success": True, "message": overview})
        
    except Profile.DoesNotExist:
        return JsonResponse({"error": "User profile not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@login_required
@api_view(['GET'])
def get_applied_jobs(request):
    try:
        user = request.user
        
        if user.role == 'recruiter':
            return get_recruiter_applications(request)
        
        user_profile = Profile.objects.get(email=user.email)
        applications = Application.objects.filter(applied_user=user_profile)
        
        applications_data = []
        for application in applications:
            applications_data.append({
                'job_id': application.job.job_id,
                'job_title': application.job.job_title,
                'company_name': application.job.company.company_name,
                'country': application.job.country,
                'salary': application.job.salary,
                'job_type': application.job.job_type,
                'application': application.application,
                'applied_date': application.created_at.isoformat(),
            })
        
        return JsonResponse({
            "success": True,
            "message": applications_data
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })

@login_required
@api_view(['GET'])
def get_favorite_jobs(request):
    try:
        user = request.user
        user_profile = Profile.objects.get(email=user.email)
        favorite_jobs_ids = user_profile.favorite_jobs

        favorite_jobs = []
        jobs = Job.objects.select_related('company').filter(job_id__in=favorite_jobs_ids)
        
        for job in jobs:
            favorite_jobs.append({
                'job_id': job.job_id,
                'job_title': job.job_title,
                'company_name': job.company.company_name,
                'country': job.country,
                'salary': job.salary,
                'job_type': job.job_type,
                'posted_date':job.created_at,
            })
        
        return JsonResponse({
            "success": True,
            "message": favorite_jobs
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        })
    
@login_required
@api_view(['GET'])
def get_recruiter_applications(request):
    try:
        user = request.user
        if user.role != 'recruiter':
            return JsonResponse({
                "success": False,
                "message": "Only recruiters can access this endpoint"
            }, status=403)


        recruiter_profile = Profile.objects.get(email=user.email)
        
        applications = Application.objects.select_related(
            'job', 'applied_user', 'company'
        ).filter(company=recruiter_profile)

        applications_data = []
        for application in applications:
            applications_data.append({
                'application_id': application.app_id,
                'job_id': application.job.job_id,
                'job_title': application.job_title,
                'candidate_name': application.applied_user.full_name,
                'candidate_email': application.applied_user.email,
                'candidate_country': application.applied_user.country,
                'application_text': application.application,
                'resume_url': application.resume,
                'applied_date': application.created_at.isoformat(),
                'candidate_profile_image': application.applied_user.profile_image_url,
                'candidate_title': application.applied_user.title,
            })

        return JsonResponse({
            "success": True,
            "message": applications_data
        })
    
    except Profile.DoesNotExist:
        return JsonResponse({
            "success": False,
            "message": "Recruiter profile not found"
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)