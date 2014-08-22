#!/bin/env python

# time datetime test

'''
python中时间日期格式化符号：

%y 两位数的年份表示                         (00-99)
%Y 四位数的年份表示                         (0000-9999)
%m 月份                                     (01-12)
%d 月内中的一天                             (0-31)
%H 24小时制小时数                           (0-23)
%I 12小时制小时数                           (01-12) 
%M 分钟数                                   (00=59)
%S 秒                                       (00-59)

%a 本地简化星期名称                         (Fri)
%A 本地完整星期名称                         (Friday)
%b 本地简化的月份名称                       (Aug)
%B 本地完整的月份名称                       (August)
%c 本地相应的日期表示和时间表示             (Fri Aug 22 16:39:48 2014) IN CentOS6.3
%j 年内的一天                               (001-366)
%p 本地A.M.或P.M.的等价符                   (PM)
%U 一年中的星期数(00-53)星期天为星期的开始  (33)
%w 星期(0-6)，星期天为星期的开始            (5)
%W 一年中的星期数(00-53)星期一为星期的开始  (33)
%x 本地相应的日期表示                       (08/22/14) IN CentOS6.3
%X 本地相应的时间表示                       (16:42:09) IN CentOS6.3
%Z 当前时区的名称                           (CST)
%% %号本身 

'''

import time, datetime

# -*- to struct_time format -*-
#   time.struct_time(tm_year=2014, tm_mon=8, tm_mday=22, tm_hour=16, tm_min=18, tm_sec=44, tm_wday=4, tm_yday=234, tm_isdst=0)

time.localtime()

time.localtime(1317175200.0)

atime = "2011-09-28 10:00:00"
btime = '19/Aug/2014:23:56:11'

struct_time_a = time.strptime(atime, '%Y-%m-%d %H:%M:%S')
struct_time_b = time.strptime(btime, '%d/%b/%Y:%H:%M:%S')

# -*- to timestamp format -*-
#   1317175200.0

time.time()
#   1408698121.328

time.mktime(struct_time_a)

# -*- format time -*-
print time.strftime('%d/%b/%Y:%H:%M:%S', time.localtime())
