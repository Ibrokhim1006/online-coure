# Generated by Django 5.0.6 on 2024-06-06 10:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0008_coursestudent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='course.coursemodul'),
        ),
    ]
