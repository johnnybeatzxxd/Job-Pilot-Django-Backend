from django.contrib import admin
from .views import *
from django.urls import include, path

urlpatterns = [
    path('signin', signin),
    path('signup', signup),
    path('set_profile', set_profile),
    path('get_profile', get_profile),
    path('dashboard/', include('dashboard.urls')),
    path('logout', logout_view),
]