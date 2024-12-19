# Generated by Django 5.1.4 on 2024-12-19 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_profile_hourly_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='hourly_rate',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.JSONField(blank=True, default=list),
        ),
    ]