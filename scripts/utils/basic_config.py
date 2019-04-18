#!/usr/bin/python3

import subprocess

def do_mountnfs(nfsserver, src, dest):
    cmd = 'mkdir -p %s; umount %s; mount %s:%s %s' % (dest, dest, nfsserver, src, dest)
    p = subprocess.run(cmd, shell=True, timeout=10)
    if p.returncode == 0:
        print('[  OK  ] Successfully mount to NFS server')
    else:
        print('[  ERROR  ] Failed to mount NFS server')
