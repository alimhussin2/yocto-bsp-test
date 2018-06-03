#!/usr/bin/python3

import time
import os
import sys
import subprocess

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

def create_env_var():
    env_file = open('lava_dut_env', 'w')
    env_file.write('MINNOWBOARD_STATUS_FLAG=0')
    env_file.close()

def run_wait():
    pid = os.getpid()
    file_pid = "wait_child.pid"
    timeout = 0.5 # in seconds
    if os.path.exists(file_pid):
        os.remove(file_pid)
    file_pid = open(file_pid, 'w')
    file_pid.write('%s' %(pid))
    file_pid.close()
    print('IDLE  {:>6}: wait for %s seconds' .format(pid) %(timeout))
    while True:
        time.sleep(2)
        proc = subprocess.Popen(['bash', '-c', 'source lava_dut_env'], stdout=subprocess.PIPE)
        
        for line in proc.stdout:
            (key, _, value) = line.partition("=")
            os.environ[key] = value
        proc.communicate()
        print(proc.stdout)
        print(os.environ['MINNOWBOARD_STATUS_FLAG'])
        flag = os.environ['MINNOWBOARD_STATUS_FLAG']
        sys.stdout.flush()
        print('MINNOWBOARD_STATUS_FLAG = %s' % str(flag))
        if flag == "1":
            break

#create_file('/etc/profile.d/lava_dut_env.sh', 'w', 'export MINNOWBOARD_STATUS_FLAG=0')
create_env_var()
run_wait()

