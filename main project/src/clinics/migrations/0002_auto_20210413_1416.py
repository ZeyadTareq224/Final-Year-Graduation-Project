# Generated by Django 3.1.3 on 2021-04-13 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinicreview',
            name='rating',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=1),
        ),
    ]
