# Generated by Django 2.0.7 on 2018-07-23 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0012_danhmuc_ngay_sua'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baiviet',
            name='danh_muc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.Danhmuc'),
        ),
    ]
