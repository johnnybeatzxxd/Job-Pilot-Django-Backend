# Generated by Django 5.1.4 on 2024-12-21 12:01

import jobs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_id', models.CharField(default=jobs.models.generate_job_id, editable=False, max_length=8, unique=True)),
                ('job_title', models.CharField(max_length=100)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('salary_type', models.CharField(choices=[('fixed', 'Fixed'), ('hourly', 'Hourly')])),
                ('job_type', models.CharField(choices=[('remote', 'Remote'), ('on-site', 'On-site'), ('hybrid', 'Hybrid')])),
                ('level', models.CharField(choices=[('entry', 'Entry'), ('intermediate', 'Intermediate'), ('senior', 'Senior'), ('lead', 'Lead'), ('expert', 'Expert')])),
                ('maximum_applications', models.PositiveIntegerField()),
                ('salary', models.DecimalField(decimal_places=2, max_digits=15)),
                ('estimated_budget', models.DecimalField(decimal_places=2, max_digits=15)),
                ('description', models.TextField()),
                ('requirements', models.JSONField(default=list)),
                ('desirable_skills', models.JSONField(default=list, null=True)),
                ('tags', models.JSONField(default=list)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
