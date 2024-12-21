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
            'role',
            'full_name',
            'title',
            'country',
            'email',
            'bio',
            'profile_image_url',
            'favorite_jobs',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'user_email']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        if instance.role == 'candidate':
           
            data['hourly_rate'] = instance.hourly_rate
            data['skills'] = instance.skills
            data['github'] = instance.github
            data['linkedin'] = instance.linkedin
        
        elif instance.role == 'recruiter':
            
            data['company_name'] = instance.company_name
            data['company_size'] = instance.company_size
            data['industry'] = instance.industry
            data['company_website'] = instance.company_website
            data['linkedin'] = instance.linkedin
            data['twitter'] = instance.twitter
        
        return data
