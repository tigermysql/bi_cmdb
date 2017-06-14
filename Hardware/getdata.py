#coding:utf-8
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
class ResultCallback(CallbackBase):
	def v2_runner_on_ok(self, result, **kwargs):
		host = result._host
		self.data = json.dumps({host.name: result._result}, indent=4)
		# print(self.data)
def exec_ansible(module,args,host,passwords=''):	
	Options = namedtuple('Options',
			['connection',
			'remote_user',
			'module_path',
			'forks',
			'become',
#			'private_key_file',
			'become_method',
			'become_user',
			'check'])
	variable_manager = VariableManager()
	loader = DataLoader()
	options = Options(connection='smart',
			remote_user='root',
			module_path=None,
			forks=5,
			become=True,
#			private_key_file='/var/www/html/CMDB/CMDB/id_rsa',
			become_method='sudo',
			become_user='root',
			check=None)
	passwords=dict(conn_pass=passwords)
	results_callback = ResultCallback()
	inventory = Inventory(loader=loader, variable_manager=variable_manager,host_list='/etc/ansible/hosts')
	variable_manager.set_inventory(inventory)
	play_source = dict(
	    name = "ansible test",
	    hosts = host,
	    gather_facts = 'no',
		tasks = [
	            dict(action=dict(module=module,args=args), register='shell_out'),
	    	   ]
	    )
	play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
	tqm = None
	try:
		tqm = TaskQueueManager(
			inventory=inventory,
			variable_manager=variable_manager,
			loader=loader,
			options=options,
			passwords=passwords,
			stdout_callback=results_callback,
			)
		result = tqm.run(play)
	finally:
		if tqm is not None:
			tqm.cleanup()
		return json.loads(results_callback.data)
if __name__ == '__main__':
	ip = "192.168.168.1"
	print exec_ansible(module="ping",args="",host=ip)