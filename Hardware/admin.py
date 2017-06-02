from django.contrib import admin
from models import *

class HardwareAdmin(admin.ModelAdmin):
	list_dispaly = ["hdIp","hdName","hdManu","hdcod","hdtype"]

admin.site.register(Hardware,HardwareAdmin)
# Register your models here.
