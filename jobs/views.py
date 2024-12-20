from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.db.utils import IntegrityError
import json
from users.models import User, Profile
from jobs.models import Job
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
#from .serializers import ProfileSerializer
from django.middleware.csrf import get_token
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

@api_view(['POST'])
def post_job(request):

    if not request.user.is_authenticated:
        return JsonResponse({'error':'Authentication required'},status=401)
    
    if request.user.role != "recruiter":
        return JsonResponse({"error":"You dont have the permission to post jobs"},status=401)

    try:
        company_id = request.data.get('companyId')
        job_title = request.data.get('jobTitle') 
        salary_type = request.data.get('salaryType')
        job_type = request.data.get('jobType')  
        level = request.data.get('professionLevel')
        maximum_applications = request.data.get('maxApplicants')
        salary = request.data.get('salary')  
        estimated_budget = request.data.get('estimatedBudget') 
        description = request.data.get('jobDescription')  
        requirements = request.data.get('requirements')
        desirable_skills = request.data.get('desirableSkills') 
        tags = request.data.get('tags')  
        
        print(company_id)
        if not company_id:
            return JsonResponse({"error":"Profile not found."},status=401)
        
        company = Profile.objects.get(email=company_id)
        Job.objects.create(
            company=company,
            job_title=job_title,
            salary_type=salary_type.lower(),
            job_type=job_type.lower(),
            level=level.lower(),
            maximum_applications=maximum_applications,
            salary=salary,  
            estimated_budget=estimated_budget,
            description=description,
            requirements=requirements,
            desirable_skills=desirable_skills,
            tags=tags
        )
        return JsonResponse({"message":"Job posted successfully."},status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    