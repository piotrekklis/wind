# Generated by Django 2.0.5 on 2018-12-16 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wind_api', '0003_apitoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElementsReturned',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]