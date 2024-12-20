# Generated by Django 5.1.3 on 2024-12-13 06:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_githubprofile_hobby_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 1, 0, 0)),
        ),
        migrations.AddField(
            model_name='resume',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='resumes/'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='address',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
