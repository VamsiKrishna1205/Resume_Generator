# Generated by Django 5.1.3 on 2024-12-09 05:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_rename_description_workexperience_descriptions_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GitHubProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('github_link', models.URLField(blank=True)),
                ('resume', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='github_profiles', to='core.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Hobby',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobby_name', models.CharField(max_length=100)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hobbies', to='core.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_name', models.CharField(max_length=100)),
                ('proficiency', models.CharField(max_length=50)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='languages', to='core.resume')),
            ],
        ),
    ]
