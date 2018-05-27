#!/usr/bin/python3

import os
import subprocess
import time
import sys

print('LAVA now in idle mode...')
proc = subprocess.Popen(['python3', 'wait.py'])
sys.stdout.flush()
time.sleep(1)
print('Idle mode end')
sys.stdout.flush()
