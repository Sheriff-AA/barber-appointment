# Generated by Django 4.2.16 on 2024-12-08 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_type', to='profiles.profiletype', verbose_name='Profile Type'),
        ),
    ]
