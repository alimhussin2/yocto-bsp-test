#!/usr/bin/env python3

import fnmatch
import os
from datetime import datetime
from os import path, makedirs, environ

def create_archives_by_daily(archives, mode=True):
    weekday=datetime.today().isoweekday()
    year=datetime.today().year
    month=datetime.today().month
    ww=int(datetime.today().strftime("%U"))+1

    if archives is None:
        archives="/srv/data"
    if mode: mode='archives'
    else: mode='nonarchives'
    archives=archives.split("/")
    archives.append(mode)
    archives.append("%d" % year)
    archives.append("%d" % month)
    archives.append("%d" % ww)
    archives.append("%d.%d" % (ww, weekday))

    official=None
    official="/".join(archives)
    makedirs(official, exist_ok=True)

    if not path.exists(official):
        print("ERROR: Unable to create dirs %s" % official)
    else:
        print("INFO : Directory %s has been created successfully" % mode)
        return official

def get_lava_dir():
    lava_dir = []
    ldir = os.listdir('/')
    for f in ldir:
        if fnmatch.fnmatch(f, 'lava-*'):
            lava_dir.append(f)
    return lava_dir
