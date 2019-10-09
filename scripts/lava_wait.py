#!/usr/bin/python3

import os
import subprocess
import time
import sys

def create_file(dest, mode, msg):
    '''
    dest: destination of file with filename
          example: /home/root/myfile.txt
    mode: mode of open file such as 'w' for write, 'r' for read
    msg:  message to write to file.
    '''
    f = open(dest, mode)
    f.write(msg)
    f.close

print('Board boot up successfully...')
print('LAVA READY TO RUN TEST')
print('LAVA now in idle mode...')
script_dir = os.path.dirname(os.path.realpath(__file__))
idle_script = os.path.join(script_dir, "idle.sh")
proc = subprocess.call(['lava-test-case', 'wait', '--shell', 'bash', idle_script])
sys.stdout.flush()
time.sleep(10)
print('Idle mode end')
sys.stdout.flush()
