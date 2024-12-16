from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Users

# Create your views here.

@api_view(['GET'])
def signin(requests):
    return HttpResponse("hello world!")

@api_view(['GET'])
def signup(requests):
    fullname = requests.data['fullName']
    company_name = requests.data['companyName']
    type = requests.data['type']
    email = requests.data['email']
    password = requests.data['password']
    first_name = fullname.split(' ')[0]
    last_name = fullname.split(' ')[1]
    if type == 'candidate':
        is_recruiter = False
        is_candidate = True
    if type == 'recruiter':
        is_recruiter = True
        is_candidate = False
    users = Users(first_name=first_name, last_name=last_name, company_name=company_name, email=email, is_recruiter=is_recruiter, is_candidate=is_candidate)
    users.set_password(password)
    users.save()
    return HttpResponse("welcome "+fullname)