from django.contrib import admin
from .models import User,Profile
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name","email","role"]
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["full_name","title","country","hourly_rate","bio","skills"]

    
admin.site.register(User,UserAdmin)
admin.site.register(Profile,ProfileAdmin)