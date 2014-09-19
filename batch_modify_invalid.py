#!/usr/local/bin/python2.7
#-*- coding: utf-8 -*-
import MySQLdb
import string

def conn2mysql(host, user, passwd, db):
    try:
        conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, charset='utf8')   
        return conn
    except Exception, e:
        print '[connect failed] %s' % e  
        return
    
    
def handler(conn, select_sql, update_sql, inva_list):
    try:
        cur = conn.cursor()
        #select_sql = r'''SELECT room_name FROM tig_muc_room WHERE room_name LIKE '%>%' OR room_name LIKE '%<%' OR room_name LIKE '%&%' OR room_name LIKE '%\'%' OR room_name LIKE '%"%' '''
        cur.execute(select_sql)
        while True:
            res = cur.fetchone()
            if res:
                inva_str = res[0]
                if "'" in inva_str:
                    inva_str = string.replace(inva_str, "'", '\\\'')
                    #print inva_str 
                    
                inva_str_m = inva_str
                for s in inva_list:
                    if s in inva_str_m:
                        inva_str_m = string.replace(inva_str_m, s, '')
                
                re_sql = update_sql % (inva_str_m, inva_str)
                print re_sql
                
            else:
                break
    except Exception, e:
        print '[execute failed] %s' % e
        
            
def main():
    host = '192.168.100.33'
    user = 'sa_zhuj'
    passwd = 'tshowzhuj'
    db = 'tigasedb'
    inva_list = ['>','<','"','\\\'','&']
    
    select_sql = r'''SELECT room_name FROM tig_muc_room WHERE room_name LIKE '%>%' OR room_name LIKE '%<%' OR room_name LIKE '%&%' OR room_name LIKE '%\'%' OR room_name LIKE '%"%' ;'''
    update_sql_fmt = "UPDATE tig_muc_room SET room_name='%s' WHERE room_name='%s';"
    select_sql2 = r'''SELECT room_desc FROM tig_muc_room WHERE room_name LIKE '%>%' OR room_name LIKE '%<%' OR room_name LIKE '%&%' OR room_name LIKE '%\'%' OR room_name LIKE '%"%' ;'''
    update_sql_fmt2 = "UPDATE tig_muc_room SET room_desc='%s' WHERE room_desc='%s';"
    conn = conn2mysql(host, user, passwd, db)
    if conn:
        handler(conn, select_sql, update_sql_fmt, inva_list) 
        print '##====================================='
        handler(conn, select_sql2, update_sql_fmt2, inva_list)
        conn.close()
    
if __name__ == '__main__':
    
    main()