# Generated by Django 2.2.6 on 2019-10-31 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('population_search', '0005_auto_20191031_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='populationsearch',
            name='city_or_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='country_cityorstate', to='population_search.CityOrState'),
        ),
    ]
