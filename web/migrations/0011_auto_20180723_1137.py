# Generated by Django 2.0.7 on 2018-07-23 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20180723_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='danhmuc',
            name='mo_ta',
            field=models.CharField(max_length=100),
        ),
    ]