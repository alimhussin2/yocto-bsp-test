#!/usr/bin/python3

# Description: This script is used to get network interfaces,
# IP address, netmask and broadcast from device under test.
# Dependency: 
#  - netifaces
#  - paramiko
# to install use pip. Example, pip3 install paramiko

import subprocess
import json
import re
import os
from shutil import copyfile

try:
    import netifaces
except ImportError:
    print("Module netifaces not install in the system. To install use pip3 install netifaces")
    exit()

def get_interfaces():
    return netifaces.interfaces()

def get_network_info():
    iface = netifaces.interfaces()
    nets = {}
    net_info = {}
    for inet in iface:
        net_face = ''.join([i for i in inet if not i.isdigit()])
        if net_face == 'eno' or net_face == 'eth':
            addr = netifaces.ifaddresses(inet)
            net_info = addr[netifaces.AF_INET]
            net_hw = addr[netifaces.AF_LINK]
            net_info = {"interface": inet, "ipaddr": net_info[0]['addr'], "netmask": net_info[0]['netmask'], "broadcast": net_info[0]['broadcast'], "macaddr": net_hw[0]['addr']}
            nets.update(net_info)
    return nets

def get_kernel_version():
    return subprocess.check_output(['uname', '-r']).decode().strip('\n')

def get_hostname():
    return subprocess.check_output(['hostname']).decode().strip('\n')

def create_info_file(data, path, filename='board_info.json'):
    file_json = os.path.join(path, filename)
    #print(json.dumps(data, sort_keys=False, indent=4, separators=(',',': ')))
    with open(file_json, 'w') as f:
        f.write(json.dumps(data, sort_keys=False, indent=4, separators=(',',': ')))
        f.close()

def load_board_info(filename):
    print('read file %s' % filename)
    with open(filename) as f:
        data = json.load(f)
        print('read from json file')
        print('kernel: %s' % data['kernel'])
        print('ipaddr: %s' % data['network']['ipaddr'])

def get_lava_job_id():
    list_dir = [f for f in os.listdir('/') if re.match(r'lava',f)]
    return list_dir[0].replace("lava-", "")

def copy_to(src, dest, filename):
    if not os.path.exists(dest):
        print('Directory in %s is not exist. Creating it...' % dest)
        os.makedirs(dest)
        os.chmod(dest, 0o777)
    dest = os.path.join(dest, filename)
    print('copy from %s to %s' %(src, dest))
    copyfile(src, dest)

def get_user():
    return subprocess.check_output(['whoami']).decode().strip('\n')

def main():
    data = {"lava_job_id": get_lava_job_id(), "kernel": get_kernel_version(), "user": get_user(), "hostname": get_hostname(), "network": get_network_info()}
    path = '/home/root'
    json_file = 'board_info.json'
    create_info_file(data, path, json_file)
    print('Board info was created at %s' % (os.path.join(path, json_file)))
    #load_board_info(os.path.join(path, json_file))
    dest_board_info = '/srv/data/LAVA/lava-job/' + get_lava_job_id()
    copy_to(os.path.join(path, json_file), dest_board_info ,'board_info.json')

main()
