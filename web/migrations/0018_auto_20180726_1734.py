# Generated by Django 2.0.7 on 2018-07-26 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0017_auto_20180726_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nguoidung',
            name='anh_dai_dien',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]
