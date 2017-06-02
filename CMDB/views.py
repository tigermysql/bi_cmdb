#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

# 登陆验证装饰器
def loginAuth(func):
	def inner(request,*args,**kw):
		try:	
			cookie_name = request.COOKIES["username"]	#验证cookie
			if cookie_name:
				return func(request,*args,**kw)
		except:
			return HttpResponseRedirect("/User/login")
	return inner

@loginAuth
def index(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	return render_to_response("index.html",locals())
		
def logout(request):
	try:
		del request.COOKIES["username"]
		del request.session["username"]
		del request.session["userid"]
	except:
		pass
	return HttpResponseRedirect("/User/login",locals())

def test(request):
	return render_to_response("test.html",locals())