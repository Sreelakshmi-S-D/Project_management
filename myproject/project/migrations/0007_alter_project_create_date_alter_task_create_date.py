# Generated by Django 5.0 on 2024-01-05 11:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_alter_project_create_date_alter_task_create_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 5, 17, 24, 24, 934981)),
        ),
        migrations.AlterField(
            model_name='task',
            name='create_date',
            field=models.DateField(default=datetime.datetime(2024, 1, 5, 17, 24, 24, 936981)),
        ),
    ]