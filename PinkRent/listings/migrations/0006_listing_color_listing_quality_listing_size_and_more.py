# Generated by Django 5.0.2 on 2024-04-17 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_listingreview'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='color',
            field=models.CharField(db_index=True, default='No', max_length=100, verbose_name='brand'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='quality',
            field=models.CharField(choices=[('good', 'Good'), ('likenew', 'Like new'), ('new', 'New')], default='good', max_length=10),
        ),
        migrations.AddField(
            model_name='listing',
            name='size',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='size'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='value'),
            preserve_default=False,
        ),
    ]