"""CMDB URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^index',"CMDB.views.index"),
    url(r'^Api', include("Api.urls")),
    url(r'^Hardware', include("Hardware.urls")),
    url(r'^Log', include("Log.urls")),
    url(r'^User', include("User.urls")),
    url(r'^Ansible', include("Ansible.urls")),
    url(r'^Rsa',include("Rsa.urls")),
    # url(r'^cookietest', "CMDB.views.cookietest"),
    # url(r'^sessiontest', "CMDB.views.sessiontest"),
    url(r'^logout', "CMDB.views.logout"),
    url(r'^test',"CMDB.views.test"),
]
