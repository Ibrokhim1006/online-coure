# Generated by Django 5.0.6 on 2024-06-06 10:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_alter_course_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodul',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cours', to='course.course'),
        ),
    ]
