from django.conf.urls import include, url
from views import *

urlpatterns = [
	url(r'index$',index),
	url(r'roles$',roles),
	url(r'cmd$',cmd),
	url(r'service$',service),
	url(r'operation/',operation),
]