from django.contrib import admin
from .views import *
from django.urls import include, path

urlpatterns = [
    path('signin', signin),
    path('signup', signup),
]