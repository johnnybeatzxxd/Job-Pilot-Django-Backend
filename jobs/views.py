from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.db.utils import IntegrityError
import json
from users.models import User, Profile
from jobs.models import Job
#from .serializers import ProfileSerializer
from django.contrib.auth.decorators import login_required
from django.db.models import Q

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
            jobs = jobs.filter(
                Q(job_title__icontains=query) |
                Q(tags__icontains=query)
            )

        if filters.get('experienceLevel'):
            jobs = jobs.filter(level=filters['experienceLevel'].lower())

        if filters.get('jobType'):
            job_types = filters['jobType']
            if isinstance(job_types, str):
                job_types = [job_types]
            
            # First check if it's a salary type
            salary_types = ['fixed', 'hourly']
            job_location_types = ['remote', 'on-site', 'hybrid']
            
            # Filter by salary type if present
            salary_type_filters = [jt.lower() for jt in job_types if jt.lower() in salary_types]
            if salary_type_filters:
                jobs = jobs.filter(salary_type__in=salary_type_filters)
            
            # Filter by job location type if present
            job_location_filters = [jt.lower() for jt in job_types if jt.lower() in job_location_types]
            if job_location_filters:
                jobs = jobs.filter(job_type__in=job_location_filters)

        if country_code and country_code != 'ALL':
            jobs = jobs.filter(country__icontains=country_code)

        price_range = filters.get('priceRange', {})
        
        # Handle fixed salary range with case insensitive salary_type
        fixed = price_range.get('fixed', {})
        if fixed.get('min') or fixed.get('max'):
            budget_filter = Q(salary_type='fixed')
            if fixed.get('min'):
                budget_filter &= Q(estimated_budget__gte=float(fixed['min']))
            if fixed.get('max'):
                budget_filter &= Q(estimated_budget__lte=float(fixed['max']))
            jobs = jobs.filter(budget_filter)

        # Handle hourly salary range with case insensitive salary_type
        hourly = price_range.get('hourly', {})
        if hourly.get('min') or hourly.get('max'):
            salary_filter = Q(salary_type='hourly')
            if hourly.get('min'):
                salary_filter &= Q(salary__gte=float(hourly['min']))
            if hourly.get('max'):
                salary_filter &= Q(salary__lte=float(hourly['max']))
            jobs = jobs.filter(salary_filter)

        if filters.get('skills'):
            for skill in filters['skills']:
                jobs = jobs.filter(tags__icontains=f'"{skill}"')

       
        jobs_list = []
        for job in jobs:
            jobs_list.append({
                'id': job.job_id,
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
                'created_at':job.created_at,
                'company': {
                    'id': job.company.id,
                    'email': job.company.email,
                    'name': job.company.company_name,
                    'profile_image':job.company.profile_image_url
                }
            })

        return JsonResponse({
            'jobs': jobs_list,
            'count': len(jobs_list)
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
@api_view(['POST'])
def save_job(request):
    user = request.user
    job_id = request.data.get("jobId")
    profile = Profile.objects.get(email=user.email)
    favorite_jobs = profile.favorite_jobs

    if job_id in favorite_jobs:
        favorite_jobs.remove(job_id)
        message = 'Job removed from favorites successfully'
    else:
        favorite_jobs.append(job_id)
        message = 'Job saved to favorites successfully'

    profile.favorite_jobs = favorite_jobs
    profile.save()
    return JsonResponse({'message': message}, status=200)
