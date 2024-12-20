from django.contrib import admin
from .models import Job
# Register your models here.



class JobAdmin(admin.ModelAdmin):
    list_display = ['job_title','level','job_type','salary_type','salary']


admin.site.register(Job,JobAdmin)