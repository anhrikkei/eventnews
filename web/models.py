from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone
from django.db import connection


class groups(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)


class users(models.Model):

    username = models.CharField(primary_key=True, max_length=15)
    password = models.CharField(max_length=150, null=False)
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=70, blank=False, unique=True)
    gender = models.BooleanField(default=1)
    avatar_url = models.FileField(upload_to='uploads')
    group = models.ForeignKey('groups', on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    token = models.CharField(max_length=200)
    is_locked = models.BooleanField(default=False)


class categories(models.Model):
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    describe = models.CharField(max_length=100)
    datetime_created = models.DateField(default=timezone.now())
    datetime_updated = models.DateField(default=timezone.now())
    user = models.ForeignKey('users', on_delete=models.CASCADE)
    show_as_menu = models.BooleanField(default=False)


class posts(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    content = RichTextField('')
    datetime_created = models.DateTimeField(default=timezone.now())
    datetime_updated = models.DateTimeField(default=timezone.now())
    user = models.ForeignKey('users', on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    is_locked = models.BooleanField(default=True)
    is_hot = models.BooleanField(default=False)
    category = models.ForeignKey('categories', null=True, on_delete=models.CASCADE)

    # def data_post_date(self):
