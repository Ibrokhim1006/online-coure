# Generated by Django 5.0.6 on 2024-06-06 06:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_remove_coursemodul_files'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('files', models.FileField(blank=True, null=True, upload_to='files')),
                ('videos', models.FileField(blank=True, null=True, upload_to='vidde')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.coursemodul')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]