#!/bin/env python
# coding utf-8

LOCAL_DATA = '/root/QQWry.Dat'

LOG_PATH = '/root/sample.log'

WHITE_LIST = ['127.0.0.1',]

#FILTER_VALUES = ['40000002', '2014:23:55']

DENY_RULES = {
        'rule01':{'keyword':['40000002', '2014:23:55'], 'area':''},
        'rule02':{'keyword':['40000002', '2014:23:56'], 'area':''}, 
}