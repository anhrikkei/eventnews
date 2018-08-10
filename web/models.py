from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

class Loaiuser(models.Model):

    ma_loai = models.AutoField(primary_key= True)
    ten_loai = models.CharField(max_length= 10)


class Nguoidung(models.Model):
    
    ten_dang_nhap = models.CharField(primary_key= True, max_length= 15)
    mat_khau = models.CharField(max_length= 150, null=False)
    ho_ten = models.CharField(max_length= 50)
    email = models.EmailField(max_length=70,blank=False, unique=True)
    gioi_tinh = models.CharField(max_length= 7)
    anh_dai_dien = models.FileField(upload_to='uploads')
    loai_user = models.ForeignKey('Loaiuser', on_delete=models.CASCADE)
    mailactive = models.CharField(max_length= 200)
    xacnhan = models.CharField(max_length= 50)
    trang_thai = models.BooleanField(default=False)


class Danhmuc(models.Model):
    
    ma_danhmuc = models.AutoField(primary_key= True)
    ten_danhmuc = models.CharField(max_length= 50, unique=True)
    mo_ta = models.CharField(max_length=100)
    ngay_tao = models.DateField()
    ngay_sua = models.DateField()
    nguoi_tao = models.ForeignKey('Nguoidung', on_delete=models.CASCADE)
    is_menu = models.BooleanField(default=False)


class Baiviet(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = RichTextField('')
    datetime_created = models.DateTimeField()
    datetime_updated = models.DateTimeField()
    user = models.ForeignKey('Nguoidung', null=True, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=True)
    is_hot = models.BooleanField(default=False)
    category = models.ForeignKey('Danhmuc', null=True, on_delete=models.CASCADE)