from django.db import models

class User(models.Model):
	username = models.CharField(max_length=32)
	password = models.CharField(max_length=32)
# Create your models here.
