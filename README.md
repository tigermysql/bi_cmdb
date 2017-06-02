#centos6 apache部署django项目


##一、安装软件
###1、安装python2.7

	yum install wget git unzip openssh-server openssh openssh-clients gcc gcc-c++ readline-devel zlib-devel bzip2-devel xz-libs xz tar openssl openssl-devel pcre-devel python-devel libevent mysql-devel sqlite-devel sshpass -y
	cd /usr/local/src/
	wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz #可以从其他地址下载，这个比较慢
	tar xvf Python-2.7.12.tgz
	cd Python-2.7.12
	./configure --prefix=/usr/local/python27 CFLAGS=-fPIC
	make && make install
	ln -s /usr/local/python27/bin/python /usr/bin/python2.7
**备注：不安装zlib-devel的话，在安装setuptools时会报错。不安装openssl-devel的话，在安装django时会报错。不加CFLAGS=-fPIC参数，安装mod_wsgi时会报错**
###2、安装setuptool，pip

	cd /usr/local/src
	unzip setuptools-32.3.1.zip
	cd setuptools-32.3.1
	python2.7 setup.py install	

	cd /usr/local/src
	tar xf pip-9.0.1.tar.gz
	cd pip-9.0.1
	python2.7 setup.py install		
	ln -s /usr/local/python27/bin/pip /usr/bin/pip2

###3、项目依赖部署

	pip2 install django==1.8.2 paramiko MySQL-python psutil
	pip2 install ansible #如已安装，略
	ln -s /usr/local/python27/bin/ansible /usr/bin/ansible
	ln -s /usr/local/python27/bin/ansible-doc /usr/bin/ansible-doc
	ln -s /usr/local/python27/bin/ansible-playbook /usr/bin/ansible-playbook
	mkdir -p /etc/ansible
	cat /etc/ansible/hosts
	[test]
	192.168.112.139
	192.168.112.140
	192.168.112.141
	

###4、安装apache以及依赖
	
	yum install httpd httpd-devel apr apr-util pcre -y
	cd /usr/local/src
	wget https://pypi.python.org/packages/f2/0a/735ffcc7c5506c997f9bf930a21d9e50b90dea559553d4ec72ab5e466357/mod_wsgi-4.5.15.tar.gz
	tar xf mod_wsgi-4.5.15.tar.gz
	cd mod_wsgi-4.5.15
	./configure --with-python=/usr/local/python27/bin/python
	make && make install
	chmod 755 /usr/lib64/httpd/modules/mod_wsgi.so

###5配置django项目
####(1)、wsgi.py设置
	cd /var/www/html/CMDB/CMDB/
	vim wsgi.py

	import sys
	sys.path.append('/var/www/html/CMDB')
	
	import os
	
	from django.core.wsgi import get_wsgi_application
	
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CMDB.settings")
	
	application = get_wsgi_application()
	#注意：前两句需要自己添加，如果没有这两句，你的程序就不能正常运行了，后面的是Django自动生成的。
####(2)、虚拟主机设置

	vim /etc/httpd/conf/httpd.conf

	LoadModule wsgi_module modules/mod_wsgi.so
	<VirtualHost *:80>
	    DocumentRoot "/var/www/html/CMDB/CMDB"
	    WSGIScriptAlias / "/var/www/html/CMDB/CMDB/wsgi.py"
	    Alias /static/ "/var/www/html/CMDB/static/"
	    <Directory "/var/www/html/CMDB/CDMB">
	        AllowOverride All
	#        Require all granted
	    </Directory>
	</VirtualHost>
	
####(3)、密钥权限设置
	ssh-keygen #生成密钥对
	ssh-copy-id xxx.xxx.xxx.xxx #推送本地公钥到远程服务器
	cp -rf /root/.ssh/id_rsa /var/www/html/CMDB/CMDB/ #拷贝私钥到密钥系统目录
	cp -rf /root/.ssh/known_hosts /var/www/.ssh/known_hosts #需要apache用户下也有授信列表
	chown -R root.apache /var/www
	chmod -R 775 /var/www
	service httpd restart

###错误示例：

####1、页面报错：Unable to create local directories(/var/www/.ansible/tmp): [Errno 13] Permission denied: '/var/www/.ansible'

	给www目录及其子目录修改权限
	chown -R root.apache /var/www
	chmod -R 775 /var/www
####2、前端样式丢失的情况

	修改httpd.conf或者虚拟主机的配置文件
 	WSGIScriptAlias / "/var/www/html/CMDB/CMDB/wsgi.py"
    Alias /static/ /var/www/html/CMDB/static/  #加这一行 指定静态文件路径

####3、由于服务器没有做授信列表（不是推送公钥），仅需要ssh 连接一下 然后按yes即可

####4、如果没有密钥认证，使用密码连接的时候没有执行成功或者页面报错，原因可能是没有安装sshpass，安装即可

####5、django.core.exceptions.ImproperlyConfigured: Error loading either pysqlite2 or sqlite3 modules (tried in that order): No module named _sqlite3

	解决：
	(1)首先安装 sqlite-devel
	yum install sqlite-devel

	(2)重新编译安装Python
	./configure --prefix=/usr/local/python27 CFLAGS=-fPIC
	make
	make install
####6、apxs: command not found
	解决：
	yum install httpd-devel 
	cd /usr/locla/src
	tar xf mod_wgsi....
	cd mod_wgsi
	./configure --with-python=/usr/local/python27/bin/python
	make && make install
