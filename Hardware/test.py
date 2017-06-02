#!/usr/bin/python
#coding:utf-8
from getdata import *
ip = "192.168.112.139"
result_dict = exec_ansible(module="setup",args="",host=ip,passwords="123456")[ip]
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
print data
