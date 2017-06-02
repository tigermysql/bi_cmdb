#coding:utf-8
from django.db import models

class User(models.Model):
	username = models.CharField(max_length=32,verbose_name="用户名")
	password = models.CharField(max_length=32,verbose_name="密码")
# Create your models here.
