#coding=utf-8
import os
import json
import paramiko
from models import *
from django.shortcuts import render_to_response
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from CMDB.views import loginAuth
from Hardware.models import Hardware
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor
from rsa import *
@loginAuth
def upload(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		user = request.POST["user"]
		rsa_pub = request.POST["rsa_pub"]
		if Rsa.objects.filter(user=user):
			state = "用户已存在，如需更新公钥请到密钥用户菜单更新密钥"
		else:
			u = Rsa()
			u.user = user
			u.rsa_pub = rsa_pub
			u.save()
			state = "公钥上传成功"
	else:
		pass
	return render_to_response("rsaTemplate/upload.html",locals())

@loginAuth
def userlist_dis(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	rsadata = Rsa.objects.all()
	user_list = []
	for udata in rsadata:
		user_list.append(udata.user)	#遍历rsa_rsa表，获取所有的用户，保存到一个list中
	all_ulp = []	#定义一个包含user，len_ip(ip_list的元素个数)，ip_list的空list
	for user in user_list:	#得到存在的每个用户，用户做下面的sql查询
		# 查询rsa_userpermission表中，当用户名等于上面的user_list的中元素时，得到每个用户对应的ip
		sql="select u.id,p.ip from Rsa_rsa as u,Hardware_hardware as p,Rsa_userpermission as up where up.user_id = u.id and up.host_id = p.id and u.user = '%s';"%user
		ip_data = UserPermission.objects.raw(sql)
		ip_list = []	#定义一个用户来存放ip地址的list，因为可能一个用户对应多个ip地址，所以ip作为一个list来保存
		one_ulp = []	#定义包含单个用户的user,len_ip,ip_list的空list
		for data in ip_data:
			ip_list.append(str(data.ip))	#得到用户对应的ip地址的list
		iplist_len = len(ip_list)	#获取到ip_list的元素个数，用来前端展示
		one_ulp.append(user)	#单个用户ulp中增加用户名
		one_ulp.append(iplist_len)	#单个用户ulp中增加ip_list的元素个数
		one_ulp.append(ip_list)	#单个用户ulp中增加ip_list
		# end 此时得到的one_ulp是这样的： ['while', 2, ['192.168.112.1', '192.168.112.2']]
		all_ulp.append(one_ulp)	#所有的ulp，即每个用户对应自己可登陆的服务器数，服务器IP地址，如：[['while', 2, ['192.168.112.1', '192.168.112.2']], ['for', 1, ['192.168.112.2']]]

	return render_to_response("rsaTemplate/user_permission.html",locals())

@loginAuth
def hostlist_dis(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	hostdata = Hardware.objects.all()
	userpermission = UserPermission.objects.all()
	ip_list = []
	for pdata in hostdata:
		ip_list.append(pdata.ip)	#遍历hardware_hardware表，获取所有的服务器ip，保存到一个list中
	all_phlu = []	#定义一个包含ip，hostname,len_user(user_list的元素个数)，user_list的空list
	for ip in ip_list:	#得到存在的每个ip地址，用户做下面的sql查询
		# 查询rsa_userpermission表中，当IP地址等于上面的ip_list的中元素时，得到每个IP地址对应的一个或多个用户
		sql="select u.id,u.user,p.hostname from Rsa_rsa as u,Hardware_hardware as p,Rsa_userpermission as up where up.user_id = u.id and up.host_id = p.id and p.ip = '%s';"%ip
		user_data = UserPermission.objects.raw(sql)
		user_list = []	#定义一个用户来存放用户名的list，因为可能一个IP地址对应多个ip用户，所以用户名作为一个list来保存
		one_phlu = []	#定义包含单个IP地址的ip,hostname,len_user,user_list的空list
		for data in user_data:
			user_list.append(data.user)	#得到IP对应的用户名的list
		hostname = Hardware.objects.get(ip=ip).hostname #得到IP对应的主机名
		userlist_len = len(user_list)	#获取到user_list的元素个数，用来前端展示
		one_phlu.append(ip)	#单个IP地址phlu中增加IP地址
		one_phlu.append(hostname) #单个IP地址phlu中增加主机名
		one_phlu.append(userlist_len)	#单个IP地址phlu中增加user_list的元素个数
		one_phlu.append(user_list)	#单个IP地址phlu中增加user_list
		# end 此时得到的one_phlu是这样的： ['192.168.112.1', zabbix-server,2, ['while', 'int']]
		all_phlu.append(one_phlu)	#所有的phlu，即每个ip地址对应自己可被登陆的用户名数，用户名列表，如：[['192.168.112.1',zabbix-server,2, ['while', 'int']], ['192.168.112.2',zabbix-client,1, ['for']]]
	return render_to_response("rsaTemplate/host_permission.html",locals())

@loginAuth
def push_dis(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"] 
	rsadata = Rsa.objects.all()
	hostlist = Hardware.objects.all()
	return render_to_response("rsaTemplate/push.html",locals())

@loginAuth
def deleteData(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "GET" and request.GET:
		try:
			user = request.GET["user"]
			sql="select u.id,p.ip from Rsa_rsa as u,Hardware_hardware as p,Rsa_userpermission as up where up.user_id = u.id and up.host_id = p.id and u.user = '%s';"%user
			ip_data = UserPermission.objects.raw(sql)
			iplist = []	#定义一个用户来存放ip地址的list，因为可能一个用户对应多个ip地址，所以ip作为一个list来保存
			for data in ip_data:
				iplist.append(str(data.ip))	#得到用户对应的ip地址的list
			user_obj = Rsa.objects.filter(user=user)
			for data in user_obj:
				id = int(data.id)
				pub = data.rsa_pub
			up_obj = UserPermission.objects.filter(user_id=id)
			up_obj.delete()
			try:
				exec_keys(vars_state="absent",pub_list=pub,host_list=iplist)
				state = "删除成功"
			except:
				state = "删除失败，请检查程序日志"
			return HttpResponseRedirect("/Rsa/userlist_dis")
		except:
			ip = str(request.GET["ip"])
			iplist = []	#inventory中的host_list必须接受的是一个list，so我们把这个IP放到一个list中
			iplist.append(ip)
			sql="select u.id,u.user,p.ip from Rsa_rsa as u,Hardware_hardware as p,Rsa_userpermission as up where up.user_id = u.id and up.host_id = p.id and p.ip = '%s';"%ip
			user_data = UserPermission.objects.raw(sql)
			user_list = []	#定义一个用户来存放用户名的list，因为可能一个ip地址对应多个用户，所以用户名作为一个list来保存
			for data in user_data:
				user_list.append(data.user)	#得到IP地址对应的用户名的list

			host_obj = Hardware.objects.filter(ip=ip)
			for data in host_obj:
				id = int(data.id)	#得到IP地址的id
			pub_list = []
			for user in user_list:
				user_obj = Rsa.objects.filter(user=user)
				for data in user_obj:
					pub_list.append(data.rsa_pub)
			# host_obj.delete()
			up_obj = UserPermission.objects.filter(host_id=id)
			up_obj.delete()
			try:
				#调用ansible接口执行playbook，实现密钥的删除功能			
				exec_keys(vars_state="absent",pub_list=pub_list,host_list=iplist)
				state = "删除成功"
			except:
				state = "删除失败，请检查程序日志"
			return HttpResponseRedirect("/Rsa/hostlist_dis") 	

#用户功能==>>展示、授权、更改公钥
@loginAuth
def user_dis(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "GET" and request.GET:
		user = request.GET["user"]
	sql="select u.id,p.ip from Rsa_rsa as u,Hardware_hardware as p,Rsa_userpermission as up where up.user_id = u.id and up.host_id = p.id and u.user = '%s';"%user
	ip_data = UserPermission.objects.raw(sql)
	exist_iplist = []	# 定义一个此用户已经可以登陆的服务器ip列表
	for data in ip_data:
		exist_iplist.append(str(data.ip))
	hostdata = Hardware.objects.all()
	userpermission = UserPermission.objects.all()
	ip_list = []	# 定义一个存放所有服务器IP的列表
	for pdata in hostdata:
		ip_list.append(pdata.ip)	#遍历Hardware_hardware表，获取所有的服务器ip，保存到一个list中
	noexist_iplist = list(set(ip_list)-set(exist_iplist)) # 使用set的差集，找到未授权的ip
	return render_to_response("rsaTemplate/user.html",locals())

@loginAuth
def user_update(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		user = request.POST["user"]
		ipstr = request.POST["ip"]
		iplist = json.loads(ipstr)
		RsaDb = Rsa.objects.get(user=user)	#过滤出勾选的用户的数据
		pub = RsaDb.rsa_pub
		uid = int(RsaDb.id)	
		ipid_list = []	#定义一个存放主机id的空列表
		for ip in iplist:	#遍历前端勾选的ip地址列表
			HostDb = Hardware.objects.get(ip=ip)	#过滤出勾选的ip的数据
			ipid_list.append(int(HostDb.id))	#把勾选的主机id添加到ipid_list中

		# 把用户id，主机id写入数据库的权限表，权限表为:user_id,host_id
		for pid in ipid_list:
			if not UserPermission.objects.filter(user_id=uid,host_id=pid):
				up = UserPermission()
				up.user_id = uid
				up.host_id = pid
				up.save()
		try:
			exec_keys(vars_state="present",pub_list=pub,host_list=iplist)
			state = "增加用户权限成功"
		except:
			state = "增加失败，请检查程序"

	else:
		state = "test"
	return JsonResponse({"state":state,"pub":pub})	

@loginAuth
def rsapub_update(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		user = request.GET["user"]
		rsa_pub = request.POST["rsa_pub"]
		user_data = Rsa.objects.get(user=user)
		if user_data.rsa_pub == rsa_pub:
			state = "公钥无需重复更新"
		else:
			user_data.rsa_pub = rsa_pub
			user_data.save()
			state = "公钥更新成功"
	else:
		user = request.GET["user"]
	return render_to_response("rsaTemplate/rsapub_update.html",locals())

#主机功能==>>展示、授权
@loginAuth
def host_dis(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "GET" and request.GET:
		ip = request.GET["ip"]
	sql="select u.id,u.user,p.ip from Rsa_rsa as u,Hardware_hardware as p,Rsa_userpermission as up where up.user_id = u.id and up.host_id = p.id and p.ip = '%s';"%ip
	user_data = UserPermission.objects.raw(sql)
	exist_userlist = []	# 定义一个允许登陆此IP地址的用户列表
	for data in user_data:
		exist_userlist.append(data.user)
	rsadata = Rsa.objects.all()
	userpermission = UserPermission.objects.all()
	user_list = []	# 定义一个存放所有用户名的列表
	for udata in rsadata:
		user_list.append(udata.user)	#遍历rsa_rsa表，获取所有的用户名，保存到一个list中
	noexist_userlist = list(set(user_list)-set(exist_userlist)) # 使用set的差集，找到未授权的用户名
	return render_to_response("rsaTemplate/host.html",locals())

@loginAuth
def host_update(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		ip = request.POST["ip"]			
		iplist = []	#inventory中的host_list必须接受的是一个list，so我们把这个IP放到一个list中
		iplist.append(ip)
		userstr = request.POST["user"]
		userlist = json.loads(userstr)
		pub_list = []
		uid_list = []
		for user in userlist:
			RsaDb = Rsa.objects.get(user=user)	#过滤出勾选的用户的数据
			pub_list.append(RsaDb.rsa_pub)	#把勾选的用户的公钥存放到一个list中
			uid_list.append(int(RsaDb.id))	#把勾选的用户的id存放到一个list中
		HostDb = Hardware.objects.get(ip=ip)	#过滤出执行操作的ip的数据
		pid = int(HostDb.id)	#得到执行操作的主机id
		# 把用户id，主机id写入数据库的权限表，权限表为:user_id,host_id
		for uid in uid_list:
			if not UserPermission.objects.filter(user_id=uid,host_id=pid):
				up = UserPermission()
				up.user_id = uid
				up.host_id = pid
				up.save()
		try:
			exec_keys(vars_state="present",pub_list=pub_list,host_list=iplist)
			state = "增加用户权限成功"
		except:
			state = "增加失败，请检查程序"

	else:
		state = "test"
	return JsonResponse({"state":state})	
# Create your views here.
