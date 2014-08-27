#!/bin/env python

from random import randint
from time import sleep
from ping import quiet_ping
import Queue
import threading

def putQueue(queue, qsize):
    for i in range(qsize):
        queue.put(i)
    return queue

def getQueue(queue, tname):
    while True:
        sleep(randint(1,2))
        if not queue.empty():
            print 'Thread-%s  %d' % (tname, queue.get())
        else:
            break

def createIP():
    ip_part1 = str(randint(1,126))
    ip_part2 = str(randint(0,255))
    ip_part3 = str(randint(0,255))
    ip_part4 = str(randint(0,255))
    return '%s.%s.%s.%s' % (ip_part1, ip_part2, ip_part3, ip_part4)  

def quietPing(ip_queue, nthread):
    while True:
        try:
            if not ip_queue.empty():
                ipaddr = ip_queue.get()
                print 'Thread-%-2s %-18s %s' % (nthread, ipaddr, quiet_ping(ipaddr))
            else:
                break
        except:
            print 'exception'

def main():
    
    ip_queue = Queue.Queue(100)
    
    for i in range(100):
        ip_queue.put(createIP())
        
    #putQueue(queue, 12)
    #getQueue(queue)
    threads = []
    
    for i in range(3):
        th = threading.Thread(target=quietPing, args=(ip_queue, str(i)))
        threads.append(th)
        
    for i in range(3):
        threads[i].start()
        
    for i in range(3):
        threads[i].join()

if __name__ == '__main__':
    
    main()
