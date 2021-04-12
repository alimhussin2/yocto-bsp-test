#!/usr/bin/python3

import subprocess
import json
import shutil
import os
import re

def checkKernel():
    cmd = 'uname -r'
    kernel = subprocess.check_output(cmd, shell=True).decode().strip('\n')
    return kernel

def checkDmesg():
    cmd = 'dmesg | grep -i -E "error|fail"'
    output = []
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:
        for line in p.stdout:
            output.append(line.decode().strip('\n'))
    return output

def writeResults(filename, data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, sort_keys=False, 
                indent=4, separators=(',',': ')))
        f.close()

def get_lava_job_id():
    """
    To get lava job id, we check /lava-*. Sometimes there are lot
    of /lava-*. So need to find the latest /lava-* as current lava
    job id.
    """
    lava_id = []
    list_dir = [f for f in os.listdir('/') if re.match(r'lava',f)]
    for d in list_dir:
        print('DEBUG: lava id: %s' % d)
        lava_id.append(os.path.join('/', d))
    cur_lava_id = max(lava_id, key=os.path.getmtime).replace('/lava-', '')
    print('DEBUG: Current lava id: %s' % cur_lava_id)
    return cur_lava_id

if __name__ == '__main__':
    resultFile = 'result_sanity_test.json'
    path = '/srv/data/LAVA/lava-job'
    kernel = checkKernel()
    dmesg = checkDmesg()
    data = { "kernel" : kernel,
             "dmesg" : dmesg }
    writeResults(resultFile, data)
    lava_id = get_lava_job_id()
    dest = os.path.join(path, lava_id)
    dest = os.path.join(dest, resultFile)
    #shutil.copyfile(resultFile, dest)
    print(data)
    #print('INFO: Upload %s to %s' % (resultFile, dest))

