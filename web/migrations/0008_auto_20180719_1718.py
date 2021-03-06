# Generated by Django 2.0.7 on 2018-07-19 10:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_auto_20180719_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='baiviet',
            name='tin_hot',
            field=models.CharField(default=0, max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='baiviet',
            name='trang_thai',
            field=models.CharField(default='on', max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='baiviet',
            name='ngay_tao',
            field=models.DateField(default=datetime.datetime(2018, 7, 19, 10, 16, 59, 426281, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='danhmuc',
            name='ngay_tao',
            field=models.DateField(default=datetime.datetime(2018, 7, 19, 10, 16, 59, 426281, tzinfo=utc), verbose_name='Date'),
        ),
    ]
