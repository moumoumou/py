#!/usr/local/bin/python
#
# Usage: fab runshell:'df -h'
#        fab yuminstall:openssl-devel
#

from fabric.api import *
from fabric.colors import *

env.user= 'root'
env.roledefs = {
			'tigase': [
						't0.kktv8.com:61022',
					   	't1.kktv8.com:61022',
					   	't2.kktv8.com:61022'
				   	  ],
            'vm': [
                    'vm1',
                    'vm2',
                    'vm3'
                  ]
			}

env.password = 'helloworld'


def runshell(command):
	env.warn_only = True
	run(command)
	#print green('Success')

def yuminstall(app):
	run('yum install %s -y' % app)

def sed():
	path2file = '/etc/cron.d/sysstat'
	run("sed -i s'/10/2/' %s" % path2file)
	run("sed -i s'/53/59/' %s" % path2file)
	run('cat %s' % path2file)

def fabput():
    put('/etc/snmp/snmpd.conf', '/etc/snmp/')

'''
def passwd():
	run('echo "123456" | passwd --stdin root')
'''
