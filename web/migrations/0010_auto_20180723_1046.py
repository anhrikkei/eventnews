# Generated by Django 2.0.7 on 2018-07-23 03:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20180723_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baiviet',
            name='ngay_tao',
            field=models.DateField(default=datetime.date(2018, 7, 23), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='danhmuc',
            name='ngay_tao',
            field=models.DateField(default=datetime.date(2018, 7, 23), verbose_name='Date'),
        ),
    ]
