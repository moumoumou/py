#!/usr/local/bin/python2.7

# execute every Monday

'''
SELECT COUNT(*) FROM muc_history WHERE `timestamp` BETWEEN 1410796800000 AND 1410883200000; #16
SELECT COUNT(*) FROM muc_history WHERE `timestamp` BETWEEN 1410883200000 AND 1410969600000; #17
SELECT COUNT(*) FROM muc_history WHERE `timestamp` BETWEEN 1410969600000 AND 1411056000000; #18
SELECT COUNT(*) FROM muc_history WHERE `timestamp` BETWEEN 1411056000000 AND 1411142400000; #19
SELECT COUNT(*) FROM muc_history WHERE `timestamp` BETWEEN 1411142400000 AND 1411228800000; #20
SELECT COUNT(*) FROM muc_history WHERE `timestamp` BETWEEN 1411228800000 AND 1411315200000; #21

SELECT COUNT(*) FROM tig_muc_room WHERE create_date BETWEEN '2014-09-16 00:00:00' AND '2014-09-17 00:00:00';
SELECT COUNT(*) FROM tig_muc_room WHERE create_date BETWEEN '2014-09-17 00:00:00' AND '2014-09-18 00:00:00';
SELECT COUNT(*) FROM tig_muc_room WHERE create_date BETWEEN '2014-09-18 00:00:00' AND '2014-09-19 00:00:00';
SELECT COUNT(*) FROM tig_muc_room WHERE create_date BETWEEN '2014-09-19 00:00:00' AND '2014-09-20 00:00:00';
SELECT COUNT(*) FROM tig_muc_room WHERE create_date BETWEEN '2014-09-20 00:00:00' AND '2014-09-21 00:00:00';
SELECT COUNT(*) FROM tig_muc_room WHERE create_date BETWEEN '2014-09-21 00:00:00' AND '2014-09-22 00:00:00';

SELECT room_id, COUNT(room_id) AS counter FROM tig_muc_member GROUP BY room_id ORDER BY counter DESC LIMIT 10;

SELECT room_name, COUNT(room_name) AS counter FROM muc_history WHERE `timestamp` BETWEEN 1410796800000 AND 1411315200000 GROUP BY room_name ORDER BY counter DESC LIMIT 10;
'''

import sys
import time
import MySQLdb

def timeConversion(localtime, daysago):
    timestamp_list = []
    today_ymd = time.strftime('%Y%m%d', localtime)
    today_zero = today_ymd + '000000'
    today_zero_struct = time.strptime(today_zero, '%Y%m%d%H%M%S')
    base_ts = int(time.mktime(today_zero_struct))*1000
    timestamp_list.append(base_ts)
    counter = daysago
    while counter > 0:
        timestamp_list.append(base_ts - 86400000*counter)
        counter -= 1
    timestamp_list.sort()
    return timestamp_list
    #[21 - 28]
    
def timeConversion2(timestamp_list):
    timefmt_list = []
    for i in timestamp_list:
        timefmt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i/1000))
        timefmt_list.append(timefmt)
    return timefmt_list
    
def sortDict(adict, k_or_v):
    if k_or_v == 'k':
        pass
    elif k_or_v == 'v':
        sorted_dict = sorted(adict.items(), key=lambda x:x[1])
        return sorted_dict
    
def main():
    try:
        host = '192.168.100.33'
        port = 3306
        db = 'tigasedb'
        user = sys.argv[1]
        passwd = sys.argv[2]
    
        conn = MySQLdb.connect(host = host, port = port , user = user, passwd = passwd, db = db, charset = 'utf8')
        cursor = conn.cursor()
        
        timestamp_list = timeConversion(time.localtime(), 7)
        timefmt_list = timeConversion2(timestamp_list)
        #print timestamp_list
        #print timefmt_list
        
        sql_top_member = 'SELECT room_id, COUNT(room_id) AS counter_member FROM tig_muc_member GROUP BY room_id ORDER BY counter_member DESC LIMIT 10'
        sql_top_chat = 'SELECT room_name, COUNT(room_name) AS counter_chat FROM muc_history WHERE `timestamp` BETWEEN %d AND %d GROUP BY room_name ORDER BY counter_chat DESC LIMIT 10' % (timestamp_list[1], timestamp_list[-1])
        
        cursor.execute(sql_top_member)
        res = cursor.fetchall()
        #print res
        print 
        print ' 群成员榜 TOP10'
        print
        print ' %-9s %s %-8s' % ('group id', '|', 'members')
        print '-------------------'
        for i in res:
            print ' %-9s %s %-8d' % (i[0], '|', i[1])
            print '-------------------'
        #print dict(res)
        
        cursor.execute(sql_top_chat)
        res = cursor.fetchall()
        #print res
        print 
        print
        print
        print ' 群聊天数榜（最近一周聊天数）'
        print
        print ' %-9s %s %-8s' % ('group id', '|', 'chat')
        print '-------------------'
        for i in res:
            print ' %-9s %s %-8d' % (i[0].split('@')[0], '|', i[1])
            print '-------------------'
        #print dict(res)
        '''
        muc_history = []
        create_room = []
        print
        print '[chat record daily]'
        for i in range(len(timestamp_list)-1):
            sql = 'SELECT COUNT(*) FROM muc_history WHERE `timestamp` BETWEEN %d AND %d' % (timestamp_list[i], timestamp_list[i+1])
            #print sql
            cursor.execute(sql)
            res = cursor.fetchone()
            #print res
            print (timestamp_list[i], int(res[0]))
        '''
        
        print
        print
        print
        print ' 每日总建群数&聊天数'            
        print
        print ' %-12s | %-5s | %-5s' % ('date', 'group', 'chat')
        print '-------------------------------'
        for i in range(len(timefmt_list)-1):
            sql1 = "SELECT COUNT(*) FROM tig_muc_room WHERE create_date BETWEEN '%s' AND '%s'" % (timefmt_list[i], timefmt_list[i+1])
            sql2 = 'SELECT COUNT(*) FROM muc_history WHERE `timestamp` BETWEEN %d AND %d' % (timestamp_list[i], timestamp_list[i+1])
            #print sql
            cursor.execute(sql1)
            res1 = cursor.fetchone()
            cursor.execute(sql2)
            res2 = cursor.fetchone()
            table = (timefmt_list[i].split()[0], int(res1[0]), int(res2[0]))
            print ' %-12s | %-5d | %-5d' % (table[0], table[1], table[2])
            print '-------------------------------'
        
    except IndexError:
        print '''Usage:
    script user password''' 
    except Exception, e:
        print e
    
    finally:
        try:
            conn.close()
        except UnboundLocalError, e:
            print 'no connect closed'
    
if __name__ == '__main__':
    main()
