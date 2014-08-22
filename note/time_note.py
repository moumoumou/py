#!/bin/env python

# time datetime note

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

import time
import datetime

########
# time #
########

# -*- to struct_time format -*-
#   time.struct_time(tm_year=2014, tm_mon=8, tm_mday=22, tm_hour=16, tm_min=18, tm_sec=44, tm_wday=4, tm_yday=234, tm_isdst=0)
#   tm_wday ：Monday is 0
#
#   tm_isdst :
#   If the DST flag is 0, the time is given in the regular time zone;
#   if it is 1, the time is given in the DST time zone;
#   if it is -1, mktime() should guess based on the date and time.
#

time.localtime()

time.localtime(1317175200.0)

atime = "2011-09-28 10:00:00"
btime = '19/Aug/2014:23:56:11'

struct_time_a = time.strptime(atime, '%Y-%m-%d %H:%M:%S')
struct_time_b = time.strptime(btime, '%d/%b/%Y:%H:%M:%S')



# -*- to timestamp format -*-
#   1317175200.0

time.time()                                            # 1408698121.328

time.mktime(struct_time_a)                             # 1317175200.0


time_a = time.time()
time_b = time.mktime(time.localtime())
time_c = time_b - time_a
#print time_a
#print time_b
#print time_c



# -*- format time -*-
time.strftime('%d/%b/%Y:%H:%M:%S', time.localtime())   # 22/Aug/2014:21:20:10




time.asctime()
time.asctime(time.localtime())
#   Convert a time tuple to a string, e.g. 'Sat Jun 06 16:26:11 1998'.
#   When the time tuple is not present, current time as returned by localtime() is used.

time.ctime()
time.ctime(time.time())
#   Convert a timestamp to a string, e.g. 'Fri Aug 22 21:42:15 2014'.
#   When the timestamp is not present, current time as returned by time() is used.

time.gmtime()
#   Convert a timestamp to a struct_time format of UTC(0 timezone).
#   e.g. time.struct_time(tm_year=2014, tm_mon=8, tm_mday=22, tm_hour=13, tm_min=54, tm_sec=10, tm_wday=4, tm_yday=234, tm_isdst=0)
#   When the timestamp is not present, current time as returned by time() is used.

time.clock()
#   Use for performance testing

time.sleep()
#   Sleeping...







############
# datetime #
############
