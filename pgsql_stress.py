#!/usr/local/bin/python2.7

import psycopg2
import string
import sys
import time
import multiprocessing
from random import randint

def exeTime(func):  
    def newFunc(*args, **args2):  
        t0 = time.time()  
        #print "@%s, {%s} start" % (time.strftime("%X", time.localtime()), func.__name__)  
        back = func(*args, **args2)  
        #print "@%s, {%s} end" % (time.strftime("%X", time.localtime()), func.__name__)  
        print "%.3fs [%s]" % (time.time() - t0, func.__name__)  
        return back  
    return newFunc

def conn2pg(host, port, user, password, database):
    try:
        conn = psycopg2.connect(host = host, port = port, user = user, password = password, database = database)
        return conn
    except Exception, e:
        print 'Connection Error\n %s' % e
        
def randStr(min_length, max_length):
    ranstr = ''
    for i in range(randint(min_length, max_length)):
        ranstr += random.choice(string.letters)
    return ranstr
    
def runSQL(conn, sql):
    try:
        cur = conn.cursor()
        result = cur.execute(sql)
        conn.commit()
        return 1
    except Exception, e:
        print 'Execute failed\n %s' % e

@exeTime
def batchInsertData(conn, tbl_name ,nrow):
    '''Batch insert as a transaction'''
    try:
        cur = conn.cursor()
        for i in range(nrow):
            sql = "insert into %s(uid, a, b) values(0, 'aaaaacccccaaaaaaaaafffffffff', 'dddddddddaaaaabddddsssss')" % tbl_name
            cur.execute(sql)
        conn.commit()
            
    except Exception, e:
        print 'Batch insert failed\n %s' %e
        
class SQList():
    def __init__(self, tbl_name, low, top):
        self.sql_01 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top)) 
        self.sql_02 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top))
        self.sql_03 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top))
        self.sql_04 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top))
        self.sql_05 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top))
        self.sql_06 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top))
        self.sql_07 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top))
        self.sql_08 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top))
        self.sql_09 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top))
        self.sql_10 = 'SELECT a from %s where id = %d' % (tbl_name, randint(low, top))
        tmp_id = randint(low, top)
        self.sql_11 = 'SELECT a from %s where id between %d and %d' % (tbl_name, tmp_id, tmp_id + randint(50, 100))
        tmp_id = randint(low, top)
        self.sql_12 = 'SELECT SUM(uid) from %s where id between %d and %d' % (tbl_name, tmp_id, tmp_id + randint(50, 200))
        tmp_id = randint(low, top)
        self.sql_13 = 'SELECT a from %s where id between %d and %d order by uid' % (tbl_name, tmp_id, tmp_id + randint(50, 100))
        tmp_id = randint(low, top)
        self.sql_14 = 'SELECT DISTINCT a from %s where id between %d and %d order by a' % (tbl_name, tmp_id, tmp_id + randint(50, 100))
        self.sql_15 = 'UPDATE %s set uid=uid+1 where id = %d' % (tbl_name, randint(low, top))
        self.sql_16 = "UPDATE %s set a='aaaaaaaaaaaaabbaaaeeaaaaaaaaaaaaa' where id = %d" % (tbl_name, randint(low, top))
        self.sql_17 = 'UPDATE %s set uid=uid+1 where id = %d' % (tbl_name, randint(low, top))
        tmp_id = randint(low, top)
        self.sql_18 = 'DELETE from %s where id = %d' % (tbl_name, tmp_id)
        self.sql_19 = "INSERT INTO %s values(%d, 0, 'only for test take it easy', 'aaaaaafffffadeeeeeeeeefadfsdddddyyyyyyyyyyyyyy')" % (tbl_name, tmp_id)

@exeTime
def runTrans(conn, ran_low, ran_top, process_num):
    try:
        counter = 0
        while True:
            trans_sql_dict = SQList('stress_test', ran_low, ran_top).__dict__  
            cur = conn.cursor()
            trans_sql_key_list = trans_sql_dict.keys()
            trans_sql_key_list.sort()
            for key in trans_sql_key_list:
                #print trans_sql_dict[key]
                cur.execute(trans_sql_dict[key])
                conn.commit()
                counter += 1
    except KeyboardInterrupt:
        print 'Porcess-%d Stopped [%d committed]' % (process_num, counter)
    finally:
        conn.close()
    

def main():
    
    host = '10.0.3.107'
    port = 5432
    user = 'postgres'
    password = 'helloworld'
    database = 'example'
    #db_name = 'test'
    tbl_name = 'stress_test'
    
    #conn = conn2pg(host, port, user, password, database)
    
    sql_create_tbl = '''
                CREATE TABLE IF NOT EXISTS %s
                (
                    id serial NOT NULL PRIMARY KEY,
                    uid int NOT NULL DEFAULT 0,
                    a varchar(50), 
                    b varchar(50)
                )
                ''' % tbl_name
    sql_create_index = 'CREATE INDEX stress_test_index01 ON %s (id)' % tbl_name
                        
    sql_truncate_tbl = 'TRUNCATE TABLE %s' % tbl_name
    sql_setval = "select setval('%s_id_seq', 1, false)" % tbl_name
    
    try:
        if sys.argv[1] == 'create':
            conn = conn2pg(host, port, user, password, database)
            if runSQL(conn, sql_create_tbl):
                print 'Table Created'
            '''
            if runSQL(conn, sql_create_index):
                print 'Index Created'
            '''
            conn.close()
        
        elif sys.argv[1] == 'insert':
            conn = conn2pg(host, port, user, password, database)
            batchInsertData(conn, tbl_name ,int(sys.argv[2]))
            conn.close()
            
        elif sys.argv[1] == 'run':
            ran_low = 1
            ran_top = int(sys.argv[2]) - 1000
            num_proc = int(sys.argv[3])
            pr_pool = []
            for i in range(num_proc):
                conn = conn2pg(host, port, user, password, database)
                pr = multiprocessing.Process(target = runTrans, args=(conn, ran_low, ran_top, i))
                pr_pool.append(pr)
            for i in range(num_proc):
                pr_pool[i].start()
            for i in range(num_proc):
                pr_pool[i].join()
            
            
            #runTrans(conn, ran_low, ran_top)
        
        elif sys.argv[1] == 'drop':
            conn = conn2pg(host, port, user, password, database)
            if runSQL(conn, 'DROP table %s' % tbl_name):
                print 'Table Dropped'
            conn.close()
           
           
    except IndexError:
        print '''Usage like
        script create
        script insert 10000
        script run 10000 10(threads)
        script drop
        '''
    

if __name__ == '__main__':
    
    main()
        