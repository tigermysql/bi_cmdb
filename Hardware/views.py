#coding:utf-8
from django.shortcuts import render_to_response
from models import *
from CMDB.views import loginAuth
from django.http import JsonResponse
from getdata import exec_ansible
from CMDB.views import loginAuth
from django.http import HttpResponseRedirect
import json
def index(request):
	return render_to_response("hardwareTemplate/index.html",locals())

@loginAuth
def display(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	hardwareData = Hardware.objects.all()
	# 如果嫌更新后数据显示比较慢，可以在这个页面打开时就执行接口获取到数据
	# all_data = []
	# for data in hardwareData:
	# 	ip = data.ip     
	# 	result_dict = exec_ansible(module='setup',args='',host=ip)[ip]
	return render_to_response("hardwareTemplate/display.html",locals())

def auto_add(request,hostid):
	h = Hardware.objects.get(id=hostid)
	ip = h.ip
	result_dict = exec_ansible(module="setup",args="",host=ip)[ip]["ansible_facts"]
	hostname = result_dict['ansible_hostname']
	mac = result_dict["ansible_default_ipv4"]["macaddress"]
	code = result_dict["ansible_cmdline"]["root"]
	os = result_dict["ansible_distribution"]+result_dict["ansible_distribution_version"]
	sn = result_dict['ansible_product_serial']
	h.hostname = hostname
	h.mac = mac
	h.code = code
	h.os = os
	h.sn = sn
	h.save()	
	return HttpResponseRedirect("/Hardware/display/")

@loginAuth	
def state_update(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		ip = str(request.POST["ip"])
		hardwareData = Hardware.objects.all()
		result_dict = exec_ansible(module="setup",args="",host=ip)[ip]["ansible_facts"]
		data = {}
		sn = result_dict['ansible_product_serial']
		hostname = result_dict['ansible_hostname']
		os_kernel = result_dict['ansible_kernel']
		cpu = result_dict['ansible_processor'][0]
		cpu_count = result_dict['ansible_processor_count']
		cpu_cores = result_dict['ansible_processor_cores']
		cpu_vcpus = result_dict['ansible_processor_vcpus']
		mem = result_dict['ansible_memtotal_mb']
		mem_used = result_dict['ansible_memory_mb']['nocache']['used']
		mem_free = result_dict['ansible_memory_mb']['nocache']['free']
		data["sn"] = sn
		data["主机名"] = hostname
		data["内核"] = os_kernel
		data["cpu"] = cpu
		data["cpu_count"] = cpu_count
		data["cpu_cores"] = cpu_cores
		data["cpu个数"] = cpu_vcpus
		data["全部内存"] = str(mem)+" M"
		data["已使用内存"] = str(mem_used)+" M"
		data["剩余内存"] = str(mem_free)+ " M"
	else:	
		data = "未获取到数据"
	return JsonResponse({"data":data})
@loginAuth
def add_hardware(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		ip = str(request.POST["ip"])
		hostname = request.POST["hostname"]
		manu = request.POST["manu"]
		mac = request.POST["mac"]
		os = request.POST["os"]
		idc = request.POST["idc"]
		sn = request.POST["sn"]
		code = request.POST["code"]
		description = request.POST["description"]
		if Hardware.objects.filter(ip=ip):
			state = "%s已存在，请勿重复添加"%ip
		else:
			h = Hardware()
			h.ip = ip
			h.hostname = hostname
			h.mac = mac
			h.manu = manu
			h.code = code
			h.os = os
			h.idc = idc 
			h.sn = sn
			h.description = description
			h.save()
			state = "%s服务器添加成功"%ip
	else:
		pass
	return render_to_response("hardwareTemplate/add_hardware.html",locals())
@loginAuth
def add_hardware_batch(request):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]	
	if request.method == "POST" and request.POST:
		description = request.POST["description"].split('\n')	#以换行符分割，把str分割为list
		# desc = request.POST["description"].split('\r')
		desc_all_list = []
		exist_ip_list = []
		noexist_ip_list = []
		for i in description:
			desc_one_list = i.split()	#以空格为分割，把每个ip、hostname等等作为一个单独的list
			if Hardware.objects.filter(ip=desc_one_list[0]):
				exist_ip_list.append(desc_one_list[0])
			else:
				h = Hardware()
				# try:
					# ip = desc_one_list[0]
					# h.ip = ip
				# except:
					# state = "IP地址必填"
				h.ip = desc_one_list[0]
				h.hostname = desc_one_list[1]
				# h.mac = desc_one_list[2]
				# h.manu = desc_one_list[3]
				# h.code = desc_one_list[4]
				# h.os = desc_one_list[5]
				# h.idc = desc_one_list[6]
				# h.sn = desc_one_list[7]
				# h.description = desc_one_list[8]
				h.save()
				noexist_ip_list.append(desc_one_list[0])
		success = "%s个服务器添加成功%s"%(len(noexist_ip_list),json.dumps(noexist_ip_list))
		fail = "%s个服务器已存在%s"%(len(exist_ip_list),json.dumps(exist_ip_list))
	return render_to_response("hardwareTemplate/add_hardware_batch.html",locals())
@loginAuth
def delhost(request,hostid):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	hostdata = Hardware.objects.get(id=hostid)
	hostdata.delete()
	return HttpResponseRedirect("/Hardware/display/")
@loginAuth
def update_host(request,hostid):
	request.COOKIES["username"] and request.session["username"]
	cookie_name = request.COOKIES["username"]
	if request.method == "POST" and request.POST:
		ip = str(request.POST["ip"])
		hostname = request.POST["hostname"]
		manu = request.POST["manu"]
		mac = request.POST["mac"]
		os = request.POST["os"]
		idc = request.POST["idc"]
		sn = request.POST["sn"]
		code = request.POST["code"]
		description = request.POST["description"]
		h = Hardware.objects.get(id=hostid)
		h.ip = ip
		h.hostname = hostname
		h.mac = mac
		h.manu = manu
		h.code = code
		h.os = os
		h.idc = idc 
		h.sn = sn
		h.description = description
		h.save()
		state = "更新成功"
	return render_to_response("hardwareTemplate/update_host.html",locals())

def test(request):
	if request.method == "POST" and request.POST:
		ip = "192.168.112.139"
		result_dict = exec_ansible(module="setup",args="",host=ip)[ip]
		data = {}
		sn = result_dict["ansible_facts"]['ansible_product_serial']
		hostname = result_dict["ansible_facts"]['ansible_hostname']
		os_kernel = result_dict["ansible_facts"]['ansible_kernel']
		cpu = result_dict["ansible_facts"]['ansible_processor'][0]
		cpu_count = result_dict["ansible_facts"]['ansible_processor_count']
		cpu_cores = result_dict["ansible_facts"]['ansible_processor_cores']
		cpu_vcpus = result_dict["ansible_facts"]['ansible_processor_vcpus']
		mem = result_dict["ansible_facts"]['ansible_memtotal_mb']
		mem_used = result_dict["ansible_facts"]['ansible_memory_mb']['nocache']['used']
		mem_free = result_dict["ansible_facts"]['ansible_memory_mb']['nocache']['free']
		data["sn"] = sn
		data["主机名"] = hostname
		data["内核"] = os_kernel
		data["cpu"] = cpu
		data["cpu_count"] = cpu_count
		data["cpu_cores"] = cpu_cores
		data["cpu个数"] = cpu_vcpus
		data["全部内存"] = mem
		data["已使用内存"] = mem_used
		data["剩余内存"] = mem_free
	else:	
		data = "未获取到数据"
	return render_to_response("hardwareTemplate/test.html",locals())