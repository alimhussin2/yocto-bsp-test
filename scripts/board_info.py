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
import sys
from shutil import copyfile
from os.path import expanduser
try:
    utilsdir=os.path.join(os.path.abspath(os.path.dirname(__file__)), "utils")
    sys.path.append(utilsdir)
    from create_archives import *
except:
    print("ERROR: Unable to import module create_archives located in %s" % utilsdir)
    sys.exit(0)
#try:
#    import netifaces
#except ImportError:
#    print("Module netifaces not install in the system. To install use pip3 install netifaces")
#    exit()

# function deprecated
def get_interfaces():
    return netifaces.interfaces()

# function deprecated
def get_network_info():
    iface = netifaces.interfaces()
    nets = {}
    net_info = {}
    try:
        for inet in iface:
            net_face = ''.join([i for i in inet if not i.isdigit()])
            if net_face == 'eno' or net_face == 'eth':
                addr = netifaces.ifaddresses(inet)
                net_info = addr[netifaces.AF_INET]
                net_hw = addr[netifaces.AF_LINK]
                net_info = {"interface": inet, 
                            "ipaddr": net_info[0]['addr'], 
                            "netmask": net_info[0]['netmask'], 
                            "broadcast": net_info[0]['broadcast'], 
                            "macaddr": net_hw[0]['addr']}
                nets.update(net_info)
    except Exception as e:
        print("type error: " + str(e))
    return nets

def get_ipaddr(iface):
    cmd = "_RAW_STREAM_V4=`/sbin/ifconfig %s | \
           grep -o -E '([[:xdigit:]]{1,3}\.){3}[[:xdigit:]]{1,3}'`; \
           echo $_RAW_STREAM_V4 | awk '{print$1}'" % iface
    return subprocess.check_output(cmd, shell=True).decode().strip('\n')

def get_broadcast(iface):
    cmd = "_RAW_STREAM_V4=`/sbin/ifconfig %s | \
           grep -o -E '([[:xdigit:]]{1,3}\.){3}[[:xdigit:]]{1,3}'`; \
           echo $_RAW_STREAM_V4 | awk '{print$3}'" % iface
    return subprocess.check_output(cmd, shell=True).decode().strip('\n')

def get_macaddr(iface):
    cmd = "/sbin/ifconfig %s |grep HWaddr" % iface
    output = subprocess.check_output(cmd, shell=True).decode().strip('\n').split()
    macaddr = output[len(output)-1]
    return macaddr

def show_netinfo():
    cmd = "IFACES=`/sbin/ifconfig | \
           grep -E 'eno[0-9]|ens[0-9]|eth[0-9]|enp[0-9]'`; \
           echo $IFACES | awk  '{ print $1 }'"
    iface = subprocess.check_output(cmd, shell=True).decode().strip('\n')
    print(iface)
    net_info = {}
    net_info = {"interface": iface, 
                "ipaddr": get_ipaddr(iface), 
                "broadcast": get_broadcast(iface), 
                "macaddr": get_macaddr(iface)}
    return net_info

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
    """
    To get lava job id, we check /lava-*. Sometimes there are lot
    of /lava-*. So need to find the latest /lava-* as current lava
    job id.
    """
    lava_id = []
    list_dir = [f for f in os.listdir('/') if re.match(r'lava',f)]
    for d in list_dir:
        print('[DEBUG] lava id: %s' % d)
        lava_id.append(os.path.join('/', d))
    cur_lava_id = max(lava_id, key=os.path.getmtime).replace('/lava-', '')
    print('[DEBUG] Current lava id: %s' % cur_lava_id)
    return cur_lava_id

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

def do_mountnfs(nfsserver, src, dest):
    cmd = 'mkdir -p %s; mount %s:%s %s' % (dest, nfsserver, src, dest)
    p = subprocess.run(cmd, shell=True, timeout=10)
    if p.returncode == 0:
        print('[  OK  ] Successfully mount to NFS server')
    else:
        print('[  ERROR  ] Failed to mount NFS server')

def get_board_info(dest):
    f_board_info = os.path.join(dest, get_lava_job_id())
    return f_board_info

def update_board_info(path_board_info, data):
    b_info = os.path.join(path_board_info, 'board_info.json')
    with open(b_info) as f:
        feed = json.load(f)
    feed.update(data)
    with open(b_info, 'w') as f:
        json.dump(feed, f, sort_keys=False, indent=4, separators=(',',': '))

def get_image_info():
    items = []
    dict_meta_layers = {}
    dict_distro_info = {}
    dict_data = {}

    if not os.path.isfile('/etc/build'):
        print('WARNING: File /etc/build is not exists')
        return dict_image_info

    with open('/etc/build') as f:
        for line in f:
            if re.findall("=", line):
                items.append(line.replace(' ', '').split('='))
        f.close()

    for item in items[:2]:
        dict_distro = {item[0].rstrip('\n'): item[1].rstrip('\n')}
        dict_distro_info.update(dict_distro)

    for item in items[2:]:
        dict_layer = {item[0]: item[1].replace('--modified', '').rstrip('\n')}
        dict_meta_layers.update(dict_layer)

    dict_data.update(dict_distro_info)
    dict_data.update(dict_meta_layers)
    dict_image_info = {"image_info": dict_data}
    return dict_image_info

def create_lava_dir():
    ww_dir = create_archives_by_daily(None, True)
    lava_dir = os.path.join(ww_dir, 'lava')
    lava_id = get_lava_job_id()
    lava_path = os.path.join(lava_dir, 'lava-' + lava_id)
    if not os.path.exists(lava_path):
        os.makedirs(lava_path)
    return lava_path

if __name__ == "__main__":
    #nfsserver = sys.argv[1]
    #nfssrc = sys.argv[2]
    #dest = sys.argv[3]
    #try:
    #    do_mountnfs(nfsserver, nfssrc, dest)
    #except subprocess.TimeoutExpired:
    #    print('[  ERROR  ] NFS server not found')
    data = {"lava_job_id": get_lava_job_id(), 
            "kernel": get_kernel_version(), 
            "user": get_user(), 
            "hostname": get_hostname(), 
            "network": show_netinfo()}
    home = expanduser("~")
    json_file = 'board_info.json'
    create_info_file(data, home, json_file)
    update_board_info(home, get_image_info())
    info_file = os.path.join(home, json_file)
    print('Board info was created at %s' % (os.path.join(home, json_file)))
    #load_board_info(os.path.join(home, json_file))
    dest_board_info = get_board_info('/srv/data/LAVA/lava-job')
    copy_to(info_file, dest_board_info ,'board_info.json')
    copy_to(info_file, create_lava_dir(), 'board_info.json')

