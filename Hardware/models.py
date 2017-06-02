#coding:utf-8
from django.db import models

class Hardware(models.Model):
	ip = models.CharField(max_length=32,verbose_name="IP地址")
	hostname = models.CharField(max_length=32,verbose_name = "主机名")
	mac = models.CharField(max_length=32,verbose_name = "MAC")
	manu = models.CharField(max_length=16,verbose_name= "硬件厂商")
	code = models.CharField(max_length=32,verbose_name = "资产编号")
	os = models.CharField(max_length=32,verbose_name = "系统")
	idc = models.CharField(max_length=32,verbose_name = "机房")
	sn = models.CharField(max_length=32,verbose_name = "SN编号")
	description = models.TextField(blank=True,null=True,verbose_name = "硬件描述")

# Create your models here.
