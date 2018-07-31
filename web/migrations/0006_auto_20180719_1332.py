# Generated by Django 2.0.7 on 2018-07-19 06:32

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_auto_20180719_0922'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Quyen',
            new_name='Loaiuser',
        ),
        migrations.RenameField(
            model_name='loaiuser',
            old_name='ma_quyen',
            new_name='ma_loai',
        ),
        migrations.RenameField(
            model_name='loaiuser',
            old_name='quyen_han',
            new_name='ten_loai',
        ),
        migrations.AlterField(
            model_name='baiviet',
            name='ngay_tao',
            field=models.DateField(default=datetime.datetime(2018, 7, 19, 6, 32, 12, 238835, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='danhmuc',
            name='ngay_tao',
            field=models.DateField(default=datetime.datetime(2018, 7, 19, 6, 32, 12, 234834, tzinfo=utc), verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='nguoidung',
            name='quyen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.Loaiuser', to_field='ma_loai'),
        ),
    ]