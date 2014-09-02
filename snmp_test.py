#!/usr/bin/env python

# http://www.oserror.com/usage/370.html

import netsnmp

info = netsnmp.snmpwalk(netsnmp.VarList(netsnmp.Varbind('IF-MIB::ifInOctets')), Version=1, DestHost='localhost', Community='public')
print info 
