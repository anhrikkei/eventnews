# Generated by Django 2.0.7 on 2018-08-14 03:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0041_auto_20180814_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='datetime_created',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 14, 10, 33, 51, 627265)),
        ),
        migrations.AlterField(
            model_name='categories',
            name='datetime_updated',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 14, 10, 33, 51, 627265)),
        ),
        migrations.AlterField(
            model_name='posts',
            name='datetime_created',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 14, 10, 33, 51, 631258)),
        ),
        migrations.AlterField(
            model_name='posts',
            name='datetime_updated',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 14, 10, 33, 51, 631258)),
        ),
    ]