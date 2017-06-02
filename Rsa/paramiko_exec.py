#!/usr/bin/python2.7
#coding:utf-8
import paramiko
import json
def exec_rsa():
	host = ["192.168.112.139","192.168.112.141"]
	user = 'root'
	passwords = '123456'
	pub = "ssh-rsa AAAAB3NzaC1yc2EAAAABJQAAAQEAmu0fdHfp7YjaV/G4xwR3ncWSCFaOJj3liYzPuf8yLj0OWTunJ33z15eQg4uV0w1y/Swk/LXC6I6o3NJbsg4kjh2g08/SNE+NXKuLgfmXvc+erYEgMQQ8QSZXIZRCkvr27PRKiorkt3rNK5BNUD8PNQ7alyF9BbXUaGUxmAyM58vDtXamMDewZbgQYeU2rgXmcQx0AKfPpEADyggo4+fencPIhCCdXzGZPn08VotpJRbaYOYd75B5qdYbI4CoBqn6YB7SS72ARxCfjyvnsNQYHqjn4/FXLa6LHwbMHd2osPNurffqyu0Xyb+JTRCNF1tp835sO8OLCCAZgzJA3hBadw== rsa-key-20170524"
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	exist_ip = []
	success_ip = []
	for ip in host:
		ssh.connect(ip,22,user,passwords)
		stdin, stdout, stderr = ssh.exec_command('cat /root/.ssh/authorized_keys')
		data = json.dumps(stdout.readlines())
		pub_list = data.replace("\\n","")
		if pub in pub_list:
			exist_ip.append(ip)
			print '%s pub is exist'%ip
		else:
			success_ip.append(ip)
			stdin, stdout, stderr = ssh.exec_command('echo %s >> /root/.ssh/authorized_keys'%pub)
			print '%s pub is upload success'%ip
	ssh.close()
	success = "%s个服务器添加成功%s"%(len(success_ip),json.dumps(success_ip).replace("[","").replace(']',''))
	fail = "%s个服务器已存在%s"%(len(exist_ip),json.dumps(exist_ip).replace("[","").replace(']',''))
#	return success,fail
#exec_rsa()
