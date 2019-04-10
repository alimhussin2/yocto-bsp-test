#!/usr/bin/python3

import subprocess
import datetime

def check_glmark2():
    out = subprocess.run(['which glmark2'], shell=True)
    if not out.returncode is 0:
        print('Glmark2 not installed in this system')
        exit()

def write_file(filename, data):
    with open(filename, "w+") as f:
        f.write(data)
        f.close()

def run_glmark2(cmd, resolution, display):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%p")
    result = "%s_%s_%s.log" % (cmd, resolution.replace('-', ''), timestamp)
    if display == "wayland":
        if resolution == "--fullscreen":
           cmd = "export XDG_RUNTIME_DIR=/run/user/0; %s %s --benchmark scene | tee -a %s" % (cmd, resolution, result)
    else:
        if resolution == '--fullscreen':
            #cmd = "export DISPLAY=:0; xset s off -dpms; %s %s --benchmark scene | tee -a %s" % (cmd, resolution, result)
             cmd = "export DISPLAY=:0; xset s off -dpms; %s %s --benchmark scene" % (cmd, resolution)
             write_file(result, "cmd: " + cmd + "\n")

        else:
            cmd = "export DISPLAY=:0; xset s off -dpms; %s -s %s --benchmark scene | tee -a %s" % (cmd, resolution, result)
    for i in range(3):
        print("Test: %s of 3" %(i+1))
        print(cmd)
        #subprocess.run(cmd, shell=True)
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p, open(result, "a+") as f:
            for line in p.stdout:
                print(line)
                f.write(line)


def test_glmark2_1080p():
    run_glmark2("glmark2", "1920x1080", "X")

def test_glmark2_fullscreen():
    run_glmark2("glmark2", "--fullscreen", "X")

def test_glmark2_es2_1080p():
    run_glmark2("glmark2-es2", "1920x1080", "X")

def test_glmark2_es2_fullscreen():
    run_glmark2("glmark2-es2", "--fullscreen", "X")

def test_glmark2_wayland_fullscreen():
    run_glmark2("glmark2-wayland", "--fullscreen", "wayland")

def test_glmark2_es2_wayland_fullscreen():
    run_glmark2("glmark2-es2-wayland", "--fullscreen", "wayland")

if __name__ == "__main__":
    check_glmark2()
    check_weston = "ps | grep -i wayland"

    display_weston = subprocess.run(check_weston, shell=True)
    if display_weston.returncode == 0:
        #print("Display server is weston")
        test_glmark2_wayland_fullscreen()
        test_glmark2_es2_wayland_fullscreen()
    else:
        test_glmark2_fullscreen()
        test_glmark2_es2_fullscreen()
