# Generated by Django 2.0.5 on 2018-12-15 23:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wind_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='observation',
            unique_together={('latitude', 'longitude')},
        ),
    ]
