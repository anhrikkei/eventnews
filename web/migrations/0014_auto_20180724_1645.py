# Generated by Django 2.0.7 on 2018-07-24 09:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0013_auto_20180723_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baiviet',
            name='ngay_tao',
            field=models.DateField(default=datetime.date(2018, 7, 24), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='danhmuc',
            name='ngay_sua',
            field=models.DateField(default=datetime.date(2018, 7, 24), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='danhmuc',
            name='ngay_tao',
            field=models.DateField(default=datetime.date(2018, 7, 24), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='nguoidung',
            name='anh_dai_dien',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]
