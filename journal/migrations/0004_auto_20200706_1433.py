# Generated by Django 3.0.7 on 2020-07-06 19:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_plant_last_watered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plant',
            name='bought',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
