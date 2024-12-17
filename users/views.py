from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from django.db.utils import IntegrityError
import json
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
# Create your views here.

@api_view(['POST'])
def signin(request):
    
        json_data = list(request.data.keys())[0]  
        data = json.loads(json_data)  
        
        email = data.get('email', '')
        password = data.get('password', '')
        print(email,password)
        if not email or not password:
            return JsonResponse({"error": "Email and password are required."}, status=400)
        
        try:
            user = authenticate(request, email=email, password=password)
            print(user)
            if user:
                login(request, user)
                return JsonResponse({'message': 'Logged in successfully'}, status=200)
            else:
                return JsonResponse({"error": "Invalid email or password."}, status=401)
        except Exception as e:
            return JsonResponse({"error": "An unexpected error occurred during authentication."}, status=500)

@api_view(['POST'])
def signup(request):
    try:
        json_data = list(request.data.keys())[0]  
        data = json.loads(json_data)  
        fullname = data.get('fullName', '')
        company_name = data.get('companyName', '')
        role = data.get('role', '')

        if not role:
            return JsonResponse({"error": "Role must be set and cannot be empty."}, status=400)
        
        email = data.get('email', '')
        password = data.get('password', '')

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
        return JsonResponse({'message': 'User created successfully'}, status=201)
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)