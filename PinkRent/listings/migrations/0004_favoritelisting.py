# Generated by Django 5.0.2 on 2024-03-27 09:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0003_alter_listing_category'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteListing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_listings', to='listings.listing', verbose_name='favorite listing')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_listings', to=settings.AUTH_USER_MODEL, verbose_name='favorited_by')),
            ],
            options={
                'verbose_name': 'favorite listing',
                'verbose_name_plural': 'favorite listings',
            },
        ),
    ]
