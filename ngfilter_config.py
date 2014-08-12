#!/bin/env python
# coding utf-8

LOCAL_DATA = './QQWry.Dat'

LOG_PATH = '/root/sample.log'

WHITE_LIST = ['127.0.0.1',]

#FILTER_VALUES = ['40000002', '2014:23:55']

DENY_RULES = {
        'rule01':{'filterlist':['40000002', '2014:23:55'], 'frequency':0, 'area':''},
        'rule02':{'filterlist':['40000002', '2014:23:56'], 'frequency':0, 'area':''}, 
}
