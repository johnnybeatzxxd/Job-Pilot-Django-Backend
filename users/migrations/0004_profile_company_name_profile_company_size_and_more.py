# Generated by Django 5.1.4 on 2024-12-19 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='company_name',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='company_size',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='profile',
            name='company_website',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='github',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='industry',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('candidate', 'Candidate'), ('recruiter', 'Recruiter')], default='candidate', max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitter',
            field=models.URLField(blank=True),
        ),
    ]
