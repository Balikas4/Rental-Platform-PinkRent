# Generated by Django 5.0.2 on 2024-06-03 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0013_alter_listing_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='picture_1',
            field=models.ImageField(blank=True, null=True, upload_to='listing_pictures/'),
        ),
        migrations.AddField(
            model_name='listing',
            name='picture_2',
            field=models.ImageField(blank=True, null=True, upload_to='listing_pictures/'),
        ),
        migrations.AddField(
            model_name='listing',
            name='picture_3',
            field=models.ImageField(blank=True, null=True, upload_to='listing_pictures/'),
        ),
    ]
