# Generated by Django 3.1.3 on 2021-04-08 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210408_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_img',
            field=models.ImageField(null=True, upload_to='media/users/profiles/images/'),
        ),
    ]
