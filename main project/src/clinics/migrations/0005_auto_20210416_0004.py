# Generated by Django 3.1.3 on 2021-04-15 22:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0004_auto_20210415_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prescription',
            name='date',
        ),
        migrations.AddField(
            model_name='prescription',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='prescription',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]