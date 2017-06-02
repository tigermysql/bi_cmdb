#coding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from models import User
import time
from django.http import JsonResponse
import hashlib

def r404(request):
	return render_to_response("404.html",locals())

def login(request):
	if request.method == "POST" and request.POST:
		username = request.POST["username"]
		password = request.POST["password"]
		hash = hashlib.md5()
		hash.update(password)
		password = hash.hexdigest()
		try:
			user = User.objects.get(username=username)
			if user.username == username and user.password == password:
				response = HttpResponseRedirect("/index")
				response.set_cookie("username",username,3600)
				request.session["username"] = username
				request.session["userid"] = user.id
				return response
			else:
				state = "您输入的账号或密码错误"
		except:
			state = '用户不存在'
	else:
		return render_to_response("login.html")
	return render_to_response("login.html",locals())

def register(request):
	if request.method == "POST" and request.POST:
		try:
			username = request.POST["username"]
			password = request.POST["password"]
			hash = hashlib.md5()
			hash.update(password)
			password = hash.hexdigest()
			if username and password:
				userobj = User()
				userobj.username = username
				userobj.password = password
				userobj.save()
				return HttpResponseRedirect("/User/login")
		except:
			pass
	return render_to_response("register.html",locals())

def userValid(request):
	if request.method == "POST" and request.POST:
		try:
			username = request.POST["username"]
			if User.objects.filter(username=username):
				state = "exist"
			else:
				state = 'success'
		except:
			pass
		return JsonResponse({"state":state})
	else:
		# return render_to_response("register.html",locals())
		state = "test"
	return JsonResponse({"state":state})

def forget_password(request):
	return render_to_response("forget_password.html",locals())
# Create your views here.
