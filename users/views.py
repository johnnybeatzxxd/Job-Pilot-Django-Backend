from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.db.utils import IntegrityError
import json
from .models import User, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from .serializers import ProfileSerializer
# Create your views here.
from django.middleware.csrf import get_token

from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
def signin(request):
    try:
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        
        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status=400)
        
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            response = JsonResponse({'message': 'Logged in successfully'}, status=200)
            
          
            csrf_token = get_token(request)
            response['X-CSRFToken'] = csrf_token
            
    
            response['Access-Control-Allow-Headers'] = 'X-CSRFToken, Content-Type'
            response['Access-Control-Allow-Origin'] = 'http://localhost:5173'
            response['Access-Control-Allow-Credentials'] = 'true'
            response['Access-Control-Expose-Headers'] = 'X-CSRFToken'  
            return response
        else:
            return JsonResponse({"error": "Invalid email or password."}, status=401)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

@api_view(['POST'])
def signup(request):
    try:
        fullname = request.data.get('fullName', '')
        company_name = request.data.get('companyName', '')
        role = request.data.get('role', '')

        if not role:
            return JsonResponse({"error": "Role must be set and cannot be empty."}, status=400)
        
        email = request.data.get('email', '')
        password = request.data.get('password', '')

        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status=400)
        
        first_name, last_name = fullname.split(' ', 1) if fullname else ('', '')

        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'User with this email already exists'}, status=400)

        user = User.objects.create(
            first_name=first_name, 
            last_name=last_name, 
            company_name=company_name, 
            email=email, 
            role=role.lower(),
            password=make_password(password)
        )
        login(request, user)

        response = JsonResponse({'message': 'User created and logged in successfully'}, status=201)
        
        csrf_token = get_token(request)
        response['X-CSRFToken'] = csrf_token
    
        response['Access-Control-Allow-Headers'] = 'X-CSRFToken, Content-Type'
        response['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Expose-Headers'] = 'X-CSRFToken'  
        
        return response
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['GET'])
def logout_view(request):
    try:
        logout(request._request)

        response = JsonResponse({'message': 'Logged out successfully'}, status=200)
        
        # Set the specific origin instead of '*'
        response['Access-Control-Allow-Origin'] = 'http://localhost:5173'
        
        response['Access-Control-Allow-Headers'] = 'X-CSRFToken, Content-Type'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Expose-Headers'] = 'X-CSRFToken'  
        return response
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
    
@api_view(['POST'])
def set_profile(request):
    if not request.user.is_authenticated:
        print("User is not authenticated:", request.user)
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        role = request.data.get('role', '').lower()
        fullname = request.data.get('fullName', '')
        country = request.data.get('country', '')
        bio = request.data.get('bio', None)
        profile_image = request.data.get('profileImage', None)

        if not fullname or not country:
            return JsonResponse({"error": "Full name and country are required."}, status=400)

        profile_data = {
            'user': request.user,
            'full_name': fullname,
            'email': request.user.email,
            'country': country,
            'bio': bio,
            'profile_image': profile_image
        }

        if role == 'candidate':
            title = request.data.get('title', '')
            hourly_rate = request.data.get('hourlyRate', '')
            skills = request.data.get('skills', [])

            if not title or not hourly_rate:
                return JsonResponse({"error": "Title and hourly rate are required for candidates."}, status=400)

            profile_data.update({
                'title': title,
                'hourly_rate': hourly_rate,
                'skills': skills
            })

        elif role == 'recruiter':
            company_name = request.data.get('companyName', '')
            company_size = request.data.get('companySize', '')
            industry = request.data.get('industry', '')
            company_website = request.data.get('companyWebsite', '')
            linkedin = request.data.get('linkedin', '')
            twitter = request.data.get('twitter', '')

            if not company_name or not company_size or not industry:
                return JsonResponse({"error": "Company name, size, and industry are required for recruiters."}, status=400)

            profile_data.update({
                'company_name': company_name,
                'company_size': company_size,
                'industry': industry,
                'company_website': company_website,
                'linkedin': linkedin,
                'twitter': twitter,
                'title': 'Recruiter',
                'skills': []  
            })

        else:
            return JsonResponse({"error": "Invalid role specified."}, status=400)
        
        profile = Profile.objects.create(**profile_data)
        
        return JsonResponse({'message': 'Profile created successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['GET'])
def get_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return JsonResponse({'profile': serializer.data}, status=200)
    except Profile.DoesNotExist:
        role = request.user.role
        full_name = request.user.first_name + ' ' + request.user.last_name

        return JsonResponse({'error': 'Profile not found', 'user':{'full_name': full_name, 'role': role}}, status=404)
