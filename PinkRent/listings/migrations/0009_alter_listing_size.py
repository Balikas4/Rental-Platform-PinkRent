# Generated by Django 5.0.2 on 2024-05-27 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_tag_category_parent_listing_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='size',
            field=models.CharField(db_index=True, max_length=100, verbose_name='size'),
        ),
    ]
