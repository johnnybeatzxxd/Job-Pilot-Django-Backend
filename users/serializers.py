from rest_framework import serializers
from .models import Profile, User

class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'user_email',
            'full_name',
            'title',
            'country',
            'hourly_rate',
            'email',
            'skills',
            'bio',
            'profile_image',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user_email']
