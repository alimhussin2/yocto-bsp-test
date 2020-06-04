#!/usr/bin/python3

import sys
import os
import subprocess
import re

def check_os_version(os_name):
    f_os = "/etc/issue"

    if os.path.isfile(f_os):
        with open(f_os) as f:
            value = re.findall(r'^.+(?=\\n)', f.readline())[0]
            if os_name in value:
                return {"match": True, "value": value}
            else:
                return {"match": False, "value": value}

def check_kernel():
    cmd = "uname -a"
    kernel = subprocess.check_output(cmd, shell=True).decode().strip('\n')
    return kernel

if __name__ == "__main__":
    try:
        NFSSERVER = sys.argv[1]
    except:
        NFSSERVER = ""
    print("NFSSERVER = %s" % NFSSERVER)
    os_name = "Poky"
    os_version = check_os_version(os_name)

    if os_version["match"] is True:
        script_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        board_config = os.path.join(script_dir, "board_config")
        idle_job = os.path.join(script_dir, "lava_wait.py")
        print(os_version["value"])
        print("Kernel: %s" % check_kernel())
        cmds = ["bash %s %s" % (board_config, NFSSERVER), "python3 %s" % idle_job]
 
        for cmd in cmds:
            print(cmd)
            subprocess.run(cmd, shell=True)

    else:
        print('os version is %s' % os_version["value"])
        print(check_kernel())

