# Generated by Django 4.2.16 on 2024-10-03 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
