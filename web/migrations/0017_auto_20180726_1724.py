# Generated by Django 2.0.7 on 2018-07-26 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0016_auto_20180726_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nguoidung',
            name='mat_khau',
            field=models.CharField(max_length=150),
        ),
    ]
