# Generated by Django 5.0.2 on 2024-06-03 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0008_userprofile_city_userprofile_contact_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='contact_options',
            field=models.JSONField(blank=True, default=dict, verbose_name='contact options'),
        ),
    ]