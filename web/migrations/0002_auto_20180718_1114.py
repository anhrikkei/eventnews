# Generated by Django 2.0.7 on 2018-07-18 04:14

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baiviet',
            name='ngay_tao',
            field=models.DateField(default=datetime.datetime(2018, 7, 18, 11, 14, 43, 282253), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='danhmuc',
            name='ngay_tao',
            field=models.DateField(default=datetime.datetime(2018, 7, 18, 4, 14, 43, 282253, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='nguoidung',
            name='quyen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Quyen'),
        ),
        migrations.AlterField(
            model_name='nguoidung',
            name='ten_dang_nhap',
            field=models.CharField(max_length=15, primary_key=True, serialize=False),
        ),
    ]
