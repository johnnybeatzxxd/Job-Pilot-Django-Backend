# Generated by Django 5.1.4 on 2024-12-19 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_company_name_profile_company_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hourly_rate',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]