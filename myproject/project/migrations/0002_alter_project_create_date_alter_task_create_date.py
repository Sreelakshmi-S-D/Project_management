# Generated by Django 5.0 on 2023-12-29 08:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 29, 13, 58, 46, 583269)),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 29, 13, 58, 46, 585263)),
        ),
    ]
