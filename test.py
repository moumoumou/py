#!/bin/env python

import time

counter = 0
with open('/root/sample.log', 'r') as f:
    for line in f:
        if '' in line:
            counter +=1 

print counter