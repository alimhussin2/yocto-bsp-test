#!/usr/bin/python3

# Description: This script is used to get network interfaces,
# IP address, netmask and broadcast from device under test.
# Dependency: 
#  - netifaces
#  - paramiko
# to install use pip. Example, pip3 install paramiko

import netifaces
import subprocess
import json
import re
import os

def get_interfaces():
    net = netifaces.interfaces()
    print(net)
    return net

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
    return subprocess.check_output(['uname', '-r']).decode()

def get_hostname():
    return subprocess.check_output(['hostname']).decode()

def create_info_file(data, path, filename='board_info.json'):
    file_json = os.path.join(path, filename)
    print(json.dumps(data, sort_keys=False, indent=4, separators=(',',': ')))
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

def main():
    #get_interfaces()
    net_info = {}
    net_info = get_network_info()
    kernel = get_kernel_version()
    hostname = get_hostname()
    job_id = get_lava_job_id()
    data = {"job_id": job_id, "kernel": kernel, "hostname": hostname, "network": net_info}
    path = '/home/root'
    json_file = 'board_info.json'
    create_info_file(data, path, json_file)
    print('Board info was created at %s' % (os.path.join(path, json_file)))
    #load_board_info(os.path.join(path, json_file))

main()
