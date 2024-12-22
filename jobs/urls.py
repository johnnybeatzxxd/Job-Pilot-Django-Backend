from django.contrib import admin
from .views import *
from django.urls import include, path

urlpatterns = [
    path('post', post_job),
    path('search', search_job),
    path('save', save_job),
    path('get', get_job),

]