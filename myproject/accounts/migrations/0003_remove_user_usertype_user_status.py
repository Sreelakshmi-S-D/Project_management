# Generated by Django 5.0 on 2023-12-29 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_usertype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='usertype',
        ),
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.IntegerField(default=False),
        ),
    ]