# Generated by Django 5.1.4 on 2024-12-23 07:48

import applications.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0002_initial'),
        ('users', '0002_profile_favorite_jobs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_id', models.CharField(default=applications.models.generate_job_id, editable=False, max_length=8, unique=True)),
                ('job_title', models.CharField(max_length=100)),
                ('country', models.CharField(blank=True, max_length=100)),
                ('job_salary', models.DecimalField(decimal_places=2, max_digits=15)),
                ('application', models.TextField()),
                ('resume', models.CharField(blank=True, max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('applied_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications_applied', to='users.profile')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications_company', to='users.profile')),
                ('job', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='jobs.job')),
            ],
        ),
    ]
