#!/usr/bin/python3
import os
import subprocess
flag = subprocess.Popen(['echo', "\$IDLE_FLAG"], stdout=subprocess.PIPE)
idk = flag.communicate()
print(idk)
print(os.environ['IDLE_FLAG'])

