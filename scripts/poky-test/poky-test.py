#!/usr/bin/python3

import sys
import os
import subprocess

def check_os_version(os_name):
    f_os = "/etc/issue"
    output = None

    if os.path.isfile(f_os):
        cmd = "cat %s | grep %s" % (f_os, os_name)
        output = subprocess.check_output(cmd, shell=True).decode().rstrip('\n')
    return output

def check_kernel():
    cmd = "uname -a"
    kernel = subprocess.check_output(cmd, shell=True).decode().strip('\n')
    return kernel

if __name__ == "__main__":
    NFSSERVER = sys.argv[1]
    os_name = "Poky"
    os_version = check_os_version(os_name)
    if not os_version is None:
        script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        board_config = os.path.join(script_dir, "board_config")
        idle_job = os.path.join(script_dir, "lava_wait.py")
        print(os_version)
        print("Kernel: %s" % check_kernel())
        cmds = ["bash %s %s" % (board_config, NFSSERVER), "python3 %s" % idle_job]
 
        for cmd in cmds:
            print(cmd)
            subprocess.run(cmd, shell=True)

    else:
        print('os version is %s' % os_version)
        print(check_kernel())

