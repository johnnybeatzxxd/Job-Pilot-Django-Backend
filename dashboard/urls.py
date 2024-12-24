from django.contrib import admin
from .views import *
from django.urls import include, path

urlpatterns = [
    path('overview',get_overview),
    path('applied_jobs',get_applied_jobs),
    path('favorite_jobs',get_favorite_jobs),
]