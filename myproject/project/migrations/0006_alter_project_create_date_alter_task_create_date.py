# Generated by Django 5.0 on 2023-12-29 08:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_alter_project_create_date_alter_task_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 29, 14, 21, 30, 876056)),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2023, 12, 29, 14, 21, 30, 879094)),
        ),
    ]
