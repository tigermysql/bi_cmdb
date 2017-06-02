from django.conf.urls import include, url
urlpatterns = [
	url(r'login', "User.views.login"),
	url(r'404', "User.views.r404"),
	url(r'register', "User.views.register"),
	url(r'uservalid', "User.views.userValid"),
	url(r'forget_password', "User.views.forget_password"),
]