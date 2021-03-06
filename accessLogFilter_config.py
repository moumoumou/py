﻿#!/bin/env python

LOCAL_DATA = './QQWry.Dat'

LOG_PATH = '/root/sample.log'

WHITELIST = ['106.86.78.37','113.105.139.212']

# s
INTERVAL = 600

# unlimited    'frequency':0 
# unlimited    'area':''   
# 124.115.77.251  陕西省渭南市临渭区/电信
DENY_RULES = {
        'rule01':{'filterlist':['124.115.77.251'], 'area':'陕西省渭南市临渭区/电信', 'frequency':1},
        'rule02':{'filterlist':['Android','40000002'], 'area':'', 'frequency':1}, 
}

# deny ip;
BLACKLIST_PATH = '' 

ERRORLOG_PATH = ''