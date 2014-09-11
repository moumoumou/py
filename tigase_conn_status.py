#!/usr/bin/env python

import ssh
import sys
        
def sshConn(host, port, username, password):
    try:
        sshconn = ssh.SSHClient()
        sshconn.set_missing_host_key_policy(ssh.AutoAddPolicy())
        sshconn.connect(host, port, username, password)
        return sshconn
        
    except Exception, e:
        print '[%s] %s' % (e.__class__.__name__, e) 
        return 0

def sshRunCmd(sshconn, command):
    stdin, stdout, stderr = sshconn.exec_command(command)
    r_stdout = stdout.read()
    r_stderr = stderr.read()
    
    if r_stdout:
        return r_stdout
    if r_stderr:
        return r_stderr
        
def main():
    try:
        host = '115.236.77.194'
        hostlist = ['115.236.77.194', '115.236.77.197', '115.236.77.198']
        port = 61022
        password = sys.argv[1]
        username = 'root'
        cmd1 = ''' netstat -antp | awk '$4 ~ ":5222" && $6 !~ "LISTEN" {++S[$6]}END{for(a in S) print a,S[a]}' '''
        cmd2 = 'cat /proc/loadavg'
    
        for host in hostlist:
            sshconn = sshConn(host, port, username, password)
            if sshconn:
                print '----------------'
                print host
                print '----------------'
                print sshRunCmd(sshconn, cmd1)
                print sshRunCmd(sshconn, cmd2)
    
            sshconn.close()
            
    except IndexError:
        print 'Please input password as first parameter'
        

if __name__ == "__main__":

    main()
            