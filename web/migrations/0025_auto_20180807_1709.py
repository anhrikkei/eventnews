# Generated by Django 2.0.7 on 2018-08-07 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0024_auto_20180801_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danhmuc',
            name='ten_danhmuc',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]