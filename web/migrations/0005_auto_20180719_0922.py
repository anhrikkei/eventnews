# Generated by Django 2.0.7 on 2018-07-19 02:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20180718_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='baiviet',
            name='luot_xem',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='baiviet',
            name='ngay_tao',
            field=models.DateField(default=datetime.datetime(2018, 7, 19, 2, 22, 16, 713093, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='danhmuc',
            name='ngay_tao',
            field=models.DateField(default=datetime.datetime(2018, 7, 19, 2, 22, 16, 706586, tzinfo=utc), verbose_name='Date'),
        ),
    ]
