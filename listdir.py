#!/usr/bin/env python

import os

allfile = []

def lstdir(path):
    for file in os.listdir(path):

        if not file.startswith('.'):       # exclude the file hiden
            fp = os.path.join(path, file)
    
            if not os.path.isdir(fp):
                #allfile.append(fp)
                pass
            else:
                allfile.append(fp)
                lstdir(fp)

    return allfile


if __name__ == '__main__':
    
    root_path = '/home/samba/workspace/tigase-server'
    allfile = lstdir(root_path)
    for file in allfile:
        print file[len(root_path):]
