# Generated by Django 5.0.2 on 2024-10-21 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0024_listing_sell_price_alter_brand_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='name_en',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='pavadinimas'),
        ),
        migrations.AddField(
            model_name='tag',
            name='name_lt',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='pavadinimas'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='quality',
            field=models.CharField(choices=[('newwithtags', 'Naujas su etiketėmis'), ('newwithouttags', 'Naujas be etikečių'), ('great', 'Puiki'), ('good', 'Gera'), ('worn', 'Vidutinė')], default='good', max_length=20),
        ),
        migrations.AlterField(
            model_name='listing',
            name='sell_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='pardavimo kaina'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='listings', to='listings.tag'),
        ),
    ]
