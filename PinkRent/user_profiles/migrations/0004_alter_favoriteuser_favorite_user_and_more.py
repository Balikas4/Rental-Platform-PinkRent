# Generated by Django 5.0.2 on 2024-03-27 09:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0003_favoriteuser'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoriteuser',
            name='favorite_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by_users', to=settings.AUTH_USER_MODEL, verbose_name='favorite user'),
        ),
        migrations.AlterField(
            model_name='favoriteuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_users', to=settings.AUTH_USER_MODEL, verbose_name='favorited_by'),
        ),
    ]
