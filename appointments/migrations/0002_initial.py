# Generated by Django 4.2.16 on 2024-11-24 02:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('barbers', '0001_initial'),
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='barber',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='barbers.barber'),
        ),
        migrations.AddField(
            model_name='rating',
            name='appointment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.appointment'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment', to='appointments.timeslot'),
        ),
        migrations.AlterUniqueTogether(
            name='timeslot',
            unique_together={('date', 'start_time', 'end_time', 'barber')},
        ),
        migrations.AlterUniqueTogether(
            name='appointment',
            unique_together={('customer_email', 'slot')},
        ),
    ]
