#coding:utf-8

import paramiko
import io
import StringIO
import os
import logging
def gen_keys(key=""):
	'''生成公钥 私钥
	'''
	output = StringIO.StringIO()
	sbuffer = StringIO.StringIO()
	key_content = {}
	if not key:
		try:
			key = paramiko.RSAKey.generate(2048)
			key.write_private_key(output)
			private_key = output.getvalue()
		except IOError:
			raise IOError('gen_keys:there was an error writing to the file')
#		except SSHException:
#			raise SSHException('gen_keys:the keys is invalid')
	else:
		private_key = key
		output.write(key)
		try:
			key = RSAKey.from_private_key(output)
		except SSHException, e:
			raise SSHException(e)

	for data in [key.get_name()," ",key.get_base64()]:
		sbuffer.write(data)
	public_key = sbuffer.getvalue()+"=="
	key_content['public_key'] = public_key
	key_content['private_key'] = private_key
	logger = logging.getLogger()
	logger.info('gen_keys:  key content:%s'%key_content)
#	return key_content
#	print key_content
	print key_content["public_key"]
	print key_content["private_key"]
	
gen_keys()
