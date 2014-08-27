#!/usr/local/bin/python2.7

import telnetlib

host = '115.236.77.194'
port = 5222

try:
    th = telnetlib.Telnet(host, port=port, timeout=2)
    th.set_debuglevel(2)
    
except Exception, e:
    print e
    

