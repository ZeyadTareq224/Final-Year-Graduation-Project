# Generated by Django 3.1.3 on 2021-05-25 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinics', '0012_prescription_appointment'),
        ('tumor_prediction', '0008_auto_20210525_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='bctest',
            name='clinic',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clinics.clinic'),
        ),
    ]
