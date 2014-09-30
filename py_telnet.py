#!/usr/local/bin/python2.7

import telnetlib
import sys
from time import sleep

try:
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    while True:
        try:
            th = telnetlib.Telnet(host, port=port, timeout=2)
            th.set_debuglevel(2)
            if th:
                print 'telnet success'
            
        except Exception, e:
            print 'telnet fail [%s]' % e 
        finally:
            sleep(2)
        
except IndexError:
    print ''' Usage:
    script ip port'''
    
except KeyboardInterrupt:
    print ' occured, stop'


