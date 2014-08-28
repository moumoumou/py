#!/bin/env python

#
# Performance statistic
# 
# ip_total 272
# --------------------------
# threads |  usetime
# --------------------------
#   50    |  0.297966003418
#   20    |  0.317163944244
#   10    |  0.34256196022
#   5     |  0.422833919525
#   3     |  0.619158029556
#   2     |  1.09398913383
#   1     |  61.1227178574
# --------------------------

# ip_total 1333
# --------------------------
# threads |  usetime
# --------------------------
#   50    |  1.30968809128
#   20    |  1.28201603889
#   10    |  1.31211805344
#   5     |  1.48950099945
#   3     |  2.03393101692
#   2     |  3.68216395378
#   1     |  ???
# --------------------------


from random import randint
from time import sleep, time
from ping import quiet_ping
import Queue
import threading

def quietPing(ip_queue, nthread):
    
    while True:
        try:
            if not ip_queue.empty():
                ipaddr = ip_queue.get()
                ping_result = quiet_ping(ipaddr, timeout=1)
                print '[%s]Thread-%-2s %-18s %r' % (str(time()), nthread, ipaddr, ping_result)

            else:
                break
        except:
            print 'exception'

          
def iplistFilter():
    '''
        Filte the ip can not ping success 
    '''
    with open('./iplist.py', 'r') as iplist1:
        for ip in iplist1:
            ping_result = quiet_ping(ip, timeout=1)
            if ping_result[1]:                      # ping success
                print ping_result
                iplist_filted = open('./iplist_filted.py', 'a')
                iplist_filted.write(ip)
                iplist_filted.close()

        
def main():
    
    ip_queue = Queue.Queue()
    
    with open('./iplist_filted.py', 'r') as iplist:
        for ip in iplist:
            ip_queue.put(ip)
    
    threads = []
    
    for i in range(1):
        th = threading.Thread(target=quietPing, args=(ip_queue, str(i)))
        threads.append(th)
        
    for t in threads:
        t.start()
        
    for t in threads:
        t.join()
    
if __name__ == '__main__':
    
    startime = time()
    main()
    print time() - startime
    
    #iplistFilter()
