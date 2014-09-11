#!/bin/env python

#   table_space_list
#   table_content
#   table_title
#   status_list
#   status_statistic

import MySQLdb
from time import sleep

def conn2mysql(host, port, user, passwd, charset):
    try:
        conn = MySQLdb.connect(host = host, port = port, user = user, passwd = passwd, charset = charset)
        return conn
        
    except Exception, e:
        print '%s %s' % (e.__class__.__name__, e)
        
def getSQL(status_name):
    sql = 'show global status like "%s"' % status_name
    return sql
        
def getStatus(conn, status_list):
    try:
        status_dic = {}
        for status_name in status_list:
            sql = getSQL(status_name)
            cursor = conn.cursor()
            cursor.execute(sql)
            result = cursor.fetchone()[1]
            status_dic[status_name] = result
    except Exception, e:
        print e
        
    return status_dic

def statusDelta(status_dic1, status_dic2, gaptime):
    delta_dic = {}
    for status in status_dic1:
        delta_dic[status] = (int(status_dic2[status]) - int(status_dic1[status])) / gaptime
    return delta_dic

def lenLine(n):
    table_line_pt = ''
    for i in range(n):
        table_line_pt += '-'
    return table_line_pt

    
def viewOutput(dic, table_space_list, tag):
    '''
    tag = 'title'   ; return table_title
    tag = 'content' ; return table_content
    tag = 'line'    ; return table_line
    '''
    content_format = '|'
    for i in range(len(table_space_list)):
            #content_format += '%s|'  
            content_format += ('%-' + str(table_space_list[i]) + 's|')
    
    if tag == 'line':    
        table_line = '+'
        for i in table_space_list:
            table_line += lenLine(i) + '+'
        return table_line
        
    if tag == 'content':
        table_content = content_format % ( 
            dic['HOST'],
            dic['QPS'],
            dic['TPS'],
            dic['Com_select'],
            dic['Com_insert'],
            dic['Com_update'],
            dic['Com_delete'],
            dic['%Write'],
            dic['%Read'], 
            dic['Questions'],   
        )
                                                               
        return table_content
                                           
    if tag == 'title':
        table_title = content_format % ( 'HOST', 'QPS', 'TPS', 'Select', 'Insert', 'Update', 'Delete', '%Write', '%Read', 'Questions')
        return table_title
    

def main():
    
    host    = '192.168.100.34'
    port    = 3306
    user    = 'sa_zhuj'
    passwd  = 'tshowzhuj'
    charset = 'utf8'
    
    gaptime = 1
    
    conn = conn2mysql(host, port, user, passwd, charset)
    
    status_list = [ 
        'Queries', 
        'Questions',
        'Com_commit', 
        'Com_rollback', 
        'Com_select',
        'Com_insert',
        'Com_update',
        'Com_delete',
    ]    
    
    status_dic_last = {}
    
    output_counter = 0
    
    while True:
        try:
            result_dic = {}
            status_dic = getStatus(conn, status_list)
            
            status_statistic = statusDelta(status_dic_last, status_dic, gaptime)        # statistic data
            if status_statistic:
                
                #   handle status_statistic         
                status_statistic['TPS']    = status_statistic['Com_commit'] + status_statistic['Com_rollback']
                status_statistic['QPS']    = status_statistic['Queries']
                
                sum_SUID =  float(status_statistic['Com_update'] + status_statistic['Com_delete'] + status_statistic['Com_insert'] + status_statistic['Com_select'])
                if not sum_SUID:
                    sum_SUID = 1
                sum_write = float(status_statistic['Com_update'] + status_statistic['Com_delete'] + status_statistic['Com_insert'])
                
                status_statistic['%Read']  = round((float(status_statistic['Com_select']) / float(sum_SUID)), 2)
                status_statistic['%Write'] = round((float(sum_write) / float(sum_SUID)), 2)
                
                del status_statistic['Com_commit']
                del status_statistic['Com_rollback']
                del status_statistic['Queries']
                
                status_statistic['HOST'] = host
                
                #print status_statistic
                
                #   Output formated
                table_space_list = [16,6,6,10,10,10,10,8,8,10]
                
                if output_counter % 20 == 0:
                    if output_counter == 0:
                        print viewOutput(status_statistic, table_space_list, tag='line')
                        print viewOutput(status_statistic, table_space_list, tag='title')
                        print viewOutput(status_statistic, table_space_list, tag='line')
                        print viewOutput(status_statistic, table_space_list, tag='content')
                        print viewOutput(status_statistic, table_space_list, tag='line')
                    else:
                        print viewOutput(status_statistic, table_space_list, tag='title')
                        print viewOutput(status_statistic, table_space_list, tag='line') 
                else:
                    print viewOutput(status_statistic, table_space_list, tag='content') 
                    print viewOutput(status_statistic, table_space_list, tag='line')
                    
                
                sleep(gaptime)
                
            else:
                output_counter -= 1
                    
            output_counter += 1        
            
            status_dic_last = status_dic
            
        except ZeroDivisionError, e:
            print e
            break
            
        except KeyboardInterrupt:
            break
            
    conn.close()  
   
if __name__ == "__main__":
   
    main()
