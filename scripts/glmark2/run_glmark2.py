#!/usr/bin/python3

import subprocess
import datetime

def check_glmark2():
    out = subprocess.run(['which glmark2'], shell=True)
    if not out.returncode is 0:
        print('Glmark2 not installed in this system')
        exit()

def run_glmark2(cmd, resolution):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%p")
    result = "%s_%s_%s.log" % (cmd, resolution.replace('-', ''), timestamp)
    if resolution == '--fullscreen':
        cmd = "DISPLAY=:0 %s %s --benchmark scene | tee -a %s" % (cmd, resolution, result)
    else:
        cmd = "DISPLAY=:0 %s -s %s --benchmark scene | tee -a %s" % (cmd, resolution, result)
    for i in range(3):
        print("Test: %s of 3" %(i+1))
        print(cmd)
        subprocess.run(cmd, shell=True)

def test_glmark2_1080p():
    run_glmark2("glmark2", "1920x1080")

def test_glmark2_fullscreen():
    run_glmark2("glmark2", "--fullscreen")

def test_glmark2es_1080p():
    run_glmark2("glmark2-es2", "1920x1080")

def test_glmark2es_fullscreen():
    run_glmark2("glmark2-es2", "--fullscreen")

check_glmark2()
test_glmark2_fullscreen()
test_glmark2_1080p()
test_glmark2es_1080p()
test_glmark2es_fullscreen()
