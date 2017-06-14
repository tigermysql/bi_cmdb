from django.conf.urls import include, url
from views import *

urlpatterns = [
	url(r'index/$',index),
	url(r'display/$',display),
	url(r'auto_add/(\d{1,3})',auto_add),
	url(r'add_hardware/$',add_hardware),
	url(r'add_hardware_batch/$',add_hardware_batch),
	url(r'state_update/$',state_update),
	url(r'delhost/(\d{1,3})',delhost),	
	url(r'update_host/(\d{1,3})',update_host),	
	url(r'test',test),
]