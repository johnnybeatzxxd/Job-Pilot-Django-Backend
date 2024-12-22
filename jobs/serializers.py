from rest_framework import serializers
from jobs.models import Job
from users.models import Profile

class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='company_name')
    profile_image = serializers.CharField(source='profile_image_url')

    class Meta:
        model = Profile
        fields = ['id', 'email', 'name', 'profile_image']

class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    jobTitle = serializers.CharField(source='job_title')
    salaryType = serializers.CharField(source='salary_type')
    jobType = serializers.CharField(source='job_type')
    maxApplicants = serializers.IntegerField(source='maximum_applications')
    estimatedBudget = serializers.FloatField(source='estimated_budget')
    desirableSkills = serializers.JSONField(source='desirable_skills')
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Job
        fields = ['id', 'jobTitle', 'country', 'salaryType', 'jobType', 'level',
                 'maxApplicants', 'salary', 'estimatedBudget', 'description',
                 'requirements', 'desirableSkills', 'tags', 'created_at', 'company']