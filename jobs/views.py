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
        country = request.data.get('country')
        salary_type = request.data.get('salaryType')
        job_type = request.data.get('jobType')  
        level = request.data.get('professionLevel')
        maximum_applications = request.data.get('maxApplicants')
        salary = request.data.get('salary')  
        estimated_budget = request.data.get('estimatedBudget') 
        description = request.data.get('jobDescription')  
        requirements = request.data.get('requirements')
        desirable_skills = request.data.get('desirables') 
        tags = request.data.get('tags')  
        
        print(company_id)
        if not company_id:
            return JsonResponse({"error":"Profile not found."},status=401)
        
        company = Profile.objects.get(email=company_id)
        Job.objects.create(
            company=company,
            job_title=job_title,
            country=country,
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

@api_view(['POST'])
def get_job(request):
    try:
        data = request.data
        query = data.get('query', '').strip()
        filters = data.get('filters', {})
        country_code = data.get('countryCode')

        jobs = Job.objects.all()

        if query:
            jobs = jobs.filter(job_title__icontains=query)

        if filters.get('experienceLevel'):
            jobs = jobs.filter(level__iexact=filters['experienceLevel'].lower())

        if filters.get('jobType'):
            job_types = filters['jobType']
            if job_types:
                jobs = jobs.filter(job_type__in=[jt.lower() for jt in job_types])

    
        if country_code and country_code != 'ALL':
            jobs = jobs.filter(country__iexact=country_code)

       
        price_range = filters.get('priceRange', {})
        
       
        hourly = price_range.get('hourly', {})
        if hourly.get('min') and hourly.get('max'):
            jobs = jobs.filter(
                salary_type='hourly',
                salary__gte=float(hourly['min']),
                salary__lte=float(hourly['max'])
            )
        
        fixed = price_range.get('fixed', {})
        if fixed.get('min') and fixed.get('max'):
            jobs = jobs.filter(
                salary_type='fixed',
                estimated_budget__gte=float(fixed['min']),
                estimated_budget__lte=float(fixed['max'])
            )

        if filters.get('skills'):
            for skill in filters['skills']:
                jobs = jobs.filter(tags__icontains=skill)

       
        jobs_list = []
        for job in jobs:
            jobs_list.append({
                'id': job.id,
                'jobTitle': job.job_title,
                'country': job.country,
                'salaryType': job.salary_type,
                'jobType': job.job_type,
                'level': job.level,
                'maxApplicants': job.maximum_applications,
                'salary': job.salary,
                'estimatedBudget': job.estimated_budget,
                'description': job.description,
                'requirements': job.requirements,
                'desirableSkills': job.desirable_skills,
                'tags': job.tags,
                'company': {
                    'id': job.company.id,
                    'email': job.company.email,
                    'name': job.company.name
                }
            })

        return JsonResponse({
            'jobs': jobs_list,
            'count': len(jobs_list)
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)