# Generated by Django 5.0.6 on 2024-06-06 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authen', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='ball',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
