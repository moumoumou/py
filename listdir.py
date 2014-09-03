#!/usr/bin/env python

import os

allfile = []

def lstdir(path):
    for file in os.listdir(path):

        if not file.startswith('.'):       # exclude the file hiden
            fp = os.path.join(path, file)
    
            if not os.path.isdir(fp):
                allfile.append(fp)
            else:
                #allfile.append(fp)
                lstdir(fp)

    return allfile


if __name__ == '__main__':
    
    allfile = lstdir('/home')
    for file in allfile:
        print file
