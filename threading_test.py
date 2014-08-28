#!/bin/env python

import threading        
import Queue     
import time       

class Producer(threading.Thread):   # 定义生产者类
    
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
        
    def run(self):
        global queue                # 声明queue为全局变量
        queue.put(self.getName())   # 调用put方法将线程名添加到队列中
        print self.getName(),'put ',self.getName(),' to queue'
        
        
class Consumer(threading.Thread):   # 定义消费者类
    
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
        
    def run(self):
        global queue
        print self.getName(),'get ',queue.get(),'from queue'   
      
        
queue = Queue.Queue()               # 生成队列对象
plist = []                          # 生成者对象列表
clist = []                          # 消费者对象列表

for i in range(10):
    p = Producer('Producer' + str(i))
    plist.append(p)
    
for i in range(10):
    c = Consumer('Consumer' + str(i))
    clist.append(c)
    
for i in plist:
    i.start()
    i.join()
    
for i in clist:
    i.start()
    i.join()