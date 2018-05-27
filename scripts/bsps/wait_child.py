#!/usr/bin/python3

import time
import os
import sys

pid = os.getpid()
file_pid = 'wait_child.pid'
timeout = 3600 # in seconds

if os.path.exists(file_pid):
    os.remove(file_pid)

f = open(file_pid, 'w')
f.write('%s' %(pid))
f.close()

print('IDLE  {:>6}: wait for %s seconds' .format(pid) %(timeout))
time.sleep(timeout)
sys.stdout.flush()
