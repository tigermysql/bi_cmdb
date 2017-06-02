from django.conf.urls import include, url
from views import *

urlpatterns = [
#	url(r'index$',index),
	url(r'upload/$',upload),	
	url(r'delete/$',deleteData),
	url(r'userlist_dis/$',userlist_dis),
	url(r'hostlist_dis/$',hostlist_dis),
	url(r'push_dis/$',push_dis),	
	url(r'user_dis/$',user_dis),
	url(r'user_update/$',user_update),
	url(r'rsapub_update/$',rsapub_update),
	url(r'host_dis/$',host_dis),
	url(r'host_update/$',host_update),
]

