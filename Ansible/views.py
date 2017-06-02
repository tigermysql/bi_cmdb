#coding:utf-8
from django.shortcuts import render_to_response
import paramiko
import sys,os
from django.http import JsonResponse
from CMDB.views import loginAuth

def index(request):
	return render_to_response("ansibleTemplate/index.html")
@loginAuth
def cmd(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		ip = request.POST["ip"]
		password = request.POST["password"]
		cmd = request.POST["cmd"]
		port = 22
		user = "root"
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,port,user,password)
		stdin, stdout, stderr = ssh.exec_command(cmd)
		text = stdout.readlines()
		ssh.close()
	# return render_to_response("ansibleTemplate/test.html",locals())
	else:
		text = []
	return JsonResponse({"dataList":text})
@loginAuth
def roles(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	return render_to_response("ansibleTemplate/roles.html",locals())

@loginAuth
def service(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		ip = request.POST["ip"]
		password = request.POST["password"]
		port = 22
		user = "root"
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,port,user,password)
		stdin, stdout, stderr = ssh.exec_command('ls /etc/init.d')
		service_data = stdout.readlines()
		# a = service_data[0]
		service = []
		for i in service_data:
			service.append(i.replace('\n',''))
		tmp_result = []
		for ser in service:
			stdin, stdout, stderr = ssh.exec_command('service %s status'%ser)
			one = []
			one.append(ser)
			one.append(stdout.read().replace('\n',''))
			tmp_result.append(one)
		result = []
		a = len(tmp_result)
		for i in range(a):
			if 'is' in tmp_result[i][1]:
				result.append(tmp_result[i])
		ssh.close()
	return render_to_response("ansibleTemplate/service.html",locals())
@loginAuth
def operation(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		ip = request.POST["ip"]
		password = request.POST["password"]
		service = request.POST["service"]
		state = request.POST["state"]
		port = 22
		user = "root"
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,port,user,password)
		stdin, stdout, stderr = ssh.exec_command('service %s %s'%(service,state))
		result = stdout.readlines()
	else:
		result = "未查询到结果"
	return JsonResponse({"result":result})




