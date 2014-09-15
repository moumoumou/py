#!/usr/local/bin/python2.7

import psycopg2
import random
import string
import sys

def conn2pg(host, port, user, password, database):
    try:
        conn = psycopg2.connect(host = host, port = port, user = user, password = password, database = database)
        return conn
    except Exception, e:
        print 'Connection Error\n %s' % e
        
def randStr(min_length, max_length):
    ranstr = ''
    for i in range(random.randint(min_length, max_length)):
        ranstr += random.choice(string.letters)
    return ranstr
    
def runSQL(conn, sql):
    try:
        cur = conn.cursor()
        result = cur.execute(sql)
        conn.commit()
        return result
    except Exception, e:
        print 'Execute failed\n %s' % e

    
def batchInsertData(conn, nrow):
    try:
        cur = conn.cursor()
        for i in range(nrow):
            value_tuple = (randStr(10, 30), randStr(10, 20), randStr(10, 20), randStr(10, 20), randStr(10, 30), randStr(10, 30))
            sql = "insert into press_test(a, b, c, d, e, f, time) values('%s', '%s', '%s', '%s', '%s', '%s', now())" % value_tuple
            cur.execute(sql)
            conn.commit()
            
    except Exception, e:
        print 'Batch insert failed\n %s' %e
        

def main():
    
    host = '10.0.3.107'
    port = 5432
    user = 'postgres'
    password = 'helloworld'
    database = 'example'
    test_tbl = 'stress_test'
    
    sql_create_tbl = '''
                CREATE TABLE IF NOT EXISTS %s
                (
                    id serial NOT NULL, 
                    a varchar(50), 
                    b varchar(50), 
                    c varchar(50), 
                    d varchar(50), 
                    e varchar(50), 
                    f varchar(50), 
                    time timestamp
                )
                ''' % test_tbl
                        
    sql_truncate_tbl = 'TRUNCATE TABLE %s' % test_tbl
    sql_setval = "select setval('%s_id_seq', 1, false)" % test_tbl
    
    try:
        conn = conn2pg(host, port, user, password, database)
    
        runSQL(conn, sql_create_tbl)
        #batchInsertData(conn, 100)
    except Exception, e:
        print e
    finally:
        conn.close()
        
    
if __name__ == '__main__':
    
    main()
    