# Generated by Django 4.2.16 on 2024-12-31 04:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_appointment_customer_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='timeslot',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='customer_email',
            field=models.EmailField(max_length=254, verbose_name='Email Address'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='customer_firstname',
            field=models.CharField(max_length=45, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='customer_lastname',
            field=models.CharField(max_length=45, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='customer_phone_number',
            field=models.CharField(max_length=20, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='appointments.timeslot', verbose_name='Time Slot'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]