#!/usr/bin/python2.7
#coding:utf-8
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
def exec_keys(vars_state,pub_list,host_list,passwords=''):
	Options = namedtuple('Options',['connection','remote_user','ask_sudo_pass','verbosity','ack_pass','private_key_file','module_path','forks','become','become_method',
							'become_user','check','listhosts','listtasks','listtags','syntax','sudo_user','sudo'])	#初始化需要的对象
	variable_manager = VariableManager()	#管理变量的类，包括主机，组，扩展等变量，之前版本是在 inventory中的	
	loader = DataLoader()	#用来加载解析yaml文件或JSON内容,并且支持vault的解密
	options = Options(connection='smart',remote_user='root',ack_pass=None,private_key_file='/var/www/html/CMDB/CMDB/id_rsa',sudo_user='root',forks=50,sudo='yes',ask_sudo_pass=False,verbosity=5,module_path=None,
					become=True,become_method='sudo',become_user='root',check=None,listhosts=None,listtasks=None,listtags=None,syntax=None)
	passwords=dict(conn_pass=passwords)	#设置密码，必须是dict类型。如果ansible主机对服务器有密钥认证，则不需要密码
	inventory = Inventory(
				loader=loader,
				variable_manager=variable_manager,
				host_list=host_list
				)	#根据inventory加载对应变量，这里host_list可以是文件也可以是IP列表
	variable_manager.set_inventory(inventory)
	extra_vars = {}	#额外的参数,key.yml以及模板中的参数,对应ansible-playbook key.yml --extra-vars pub=xxx state=present/absent
	extra_vars["pub_list"] = pub_list
	extra_vars["state"] = vars_state
	variable_manager.extra_vars = extra_vars
	#playbooks填写yml文件路径，可以写多个，是个列表
	playbook = PlaybookExecutor(
					playbooks=['/var/www/html/CMDB/CMDB/key.yml'],
		        	inventory=inventory,
		    	    variable_manager=variable_manager,
			        loader=loader,
		            options=options,
				    passwords=passwords
		            )
	playbook.run()
