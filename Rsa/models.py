#coding:utf-8
from django.db import models

class Rsa(models.Model):
	user = models.CharField(max_length=32)
	rsa_pub = models.TextField()

class UserPermission(models.Model):
	user_id = models.IntegerField()
	host_id = models.IntegerField()
	delete_flag = models.CharField(max_length=4)
# Create your models here.
