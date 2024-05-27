# Generated by Django 5.0.2 on 2024-05-27 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_alter_listing_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='size',
            field=models.CharField(choices=[('XXXS / 30 / 2', 'XXXS / 30 / 2'), ('XXS / 32 / 4', 'XXS / 32 / 4'), ('XS / 34 / 6', 'XS / 34 / 6'), ('S / 36 / 8', 'S / 36 / 8'), ('M / 38 / 10', 'M / 38 / 10'), ('L / 40 / 12', 'L / 40 / 12'), ('XL / 42 / 14', 'XL / 42 / 14'), ('XXL / 44 / 16', 'XXL / 44 / 16'), ('XXXL / 46 / 18', 'XXXL / 46 / 18'), ('4XL / 48 / 20', '4XL / 48 / 20'), ('5XL / 50 / 22', '5XL / 50 / 22'), ('6XL / 52 / 24', '6XL / 52 / 24'), ('7XL / 54 / 26', '7XL / 54 / 26'), ('8XL / 56 / 28', '8XL / 56 / 28'), ('35', '35'), ('35.5', '35.5'), ('36', '36'), ('36.5', '36.5'), ('37', '37'), ('37.5', '37.5'), ('38', '38'), ('38.5', '38.5'), ('39', '39'), ('39.5', '39.5'), ('40', '40'), ('40.5', '40.5'), ('41', '41'), ('41.5', '41.5'), ('42', '42'), ('42.5', '42.5'), ('43', '43'), ('43.5', '43.5'), ('44', '44'), ('44.5', '44.5'), ('45', '45'), ('45.5', '45.5'), ('46', '46'), ('46.5', '46.5'), ('47', '47'), ('47.5', '47.5'), ('48', '48'), ('48.5', '48.5'), ('onesize', 'One Size'), ('Other', 'Other')], db_index=True, default=None, max_length=100, verbose_name='size'),
        ),
    ]
