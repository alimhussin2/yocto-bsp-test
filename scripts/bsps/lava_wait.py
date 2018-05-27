#!/usr/bin/python3

import os
import subprocess
import time
import sys

print('LAVA now in idle mode...')
#proc = subprocess.Popen(['python3', 'wait.py'])
proc = subprocess.call(['lava-test-case', 'wait', '--shell', 'python3', 'wait_child.py'])
sys.stdout.flush()
time.sleep(1)
print('Idle mode end')
sys.stdout.flush()
