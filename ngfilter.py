#!/bin/env python
# coding utf-8

import ngfilter_config as config
import re

from struct import *
import string
import platform
 
def string2ip(str):
    ss = string.split(str, '.');
    ip = 0L
    for s in ss: ip = (ip << 8) + string.atoi(s)
    return ip;
 
class IpLocater :
    def __init__(self, ipdb_file):
        self.ipdb = open(ipdb_file, "rb")
        str = self.ipdb.read(8)
        (self.first_index,self.last_index) = unpack('II',str)
        self.index_count = (self.last_index - self.first_index) / 7 + 1
 
    def getString(self,offset = 0):
        if offset :
            self.ipdb.seek(offset)
        str = ""
        ch = self.ipdb.read(1)
        (byte,) = unpack('B',ch)
        while byte != 0:
            str = str + ch
            ch = self.ipdb.read(1)
            (byte,) = unpack('B',ch) 
        return str
 
    def getLong3(self,offset = 0):
        if offset :
            self.ipdb.seek(offset)
        str = self.ipdb.read(3)
        (a,b) = unpack('HB',str)
        return (b << 16) + a
 
    def getAreaAddr(self,offset=0):
        if offset :
            self.ipdb.seek(offset)
        str = self.ipdb.read(1)
        (byte,) = unpack('B',str)
        if byte == 0x01 or byte == 0x02:
            p = self.getLong3()
            if p:
                return self.getString(p)
            else:
                return ""
        else:
            return self.getString(offset)
 
    def getAddr(self,offset ,ip = 0):
        self.ipdb.seek(offset + 4)
 
        countryAddr = ""
        areaAddr = ""
        str = self.ipdb.read(1)
        (byte,) = unpack('B',str)
        if byte == 0x01:
            countryOffset = self.getLong3()
            self.ipdb.seek(countryOffset)
            str = self.ipdb.read(1)
            (b,) = unpack('B',str)
            if b == 0x02:
                countryAddr = self.getString(self.getLong3())
                self.ipdb.seek(countryOffset + 4)
            else:
                countryAddr = self.getString(countryOffset)
            areaAddr = self.getAreaAddr()
        elif byte == 0x02:
            countryAddr = self.getString(self.getLong3())
            areaAddr = self.getAreaAddr(offset + 8)
        else:
            countryAddr = self.getString(offset + 4)
            areaAddr = self.getAreaAddr()
 
        return countryAddr + "/" + areaAddr
 
    def output(self, first ,last):
        if last > self.index_count :
            last = self.index_count
        for index in range(first,last):
            offset = self.first_index + index * 7
            self.ipdb.seek(offset)
            buf = self.ipdb.read(7)
            (ip,of1,of2) = unpack("IHB",buf)
 
    def find(self,ip,left,right):
        if right-left == 1:
            return left
        else:
            middle = (left + right) / 2
            offset = self.first_index + middle * 7
            self.ipdb.seek(offset)
            buf = self.ipdb.read(4)
            (new_ip,) = unpack("I",buf)
            if ip <= new_ip :
                return self.find(ip, left, middle)
            else:
                return self.find(ip, middle, right)
 
    def getIpAddr(self,ip):
        index = self.find(ip,0,self.index_count - 1)
        ioffset = self.first_index + index * 7
        aoffset = self.getLong3(ioffset + 4)
        address = self.getAddr(aoffset)
        return address 
        
def queryIP(ipaddr, local_data = config.LOCAL_DATA):
    ''' Return Locater Of target IP like 娴欐睙鐪佹澀宸炲競/鐢典俊 '''
    ip_locater = IpLocater(local_data)
    ip_locater.output(100, 200)
    addr = ip_locater.getIpAddr(string2ip(ipaddr))
    if platform.system() == "Linux":
        addr = unicode(addr, 'gbk').encode('utf-8')
    return addr

def filterByLine(line, deny_rules = config.DENY_RULES):
    try:
        f = open(log_path, 'r')
        for line in f:
            for rule in deny_rules:
                counter = 0 
                for kw in deny_rules[rule]['keyword']:
                    if kw in line:
                        counter += 1
                if counter == len(deny_rules[rule]['keyword']):
                    print line, 
                        	
        	'''
            counter = 0
    	    for value in filter_values:
                if value in line:
                    counter += 1
            if counter == len(filter_values):  # matched
            	pass
                #print line
            '''
    except Exception, e:
        print e


if __name__ == "__main__" :
    
    #ip = '122.224.137.162'
    
    #print '%s %s' % (ip, queryIP(ip))
    
    filterKeyWord()