#!/usr/local/bin/python2.7

import telnetlib
from time import sleep

host = '115.236.77.194'
port = 5222

while True:
    try:
        th = telnetlib.Telnet(host, port=port, timeout=2)
        th.set_debuglevel(2)
        print th
        
    except Exception, e:
        print e 
    finally:
        sleep(2)
