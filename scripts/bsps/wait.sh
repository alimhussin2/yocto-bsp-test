#!/bin/bash

timeout=5  # seconds
flag=1
create_env_file() {
echo "MINNOWBOARD_STATUS_FLAG=0" > lava_dut_env
}

read_env_file() {
cat lava_dut_env | grep MINNOWBOARD_STATUS_FLAG | cut -d '=' -f 2
}

run_timer() {
local timer=0
create_env_file
while [[ $timer -lt $timeout ]];
do
   status=$(read_env_file)
   echo "status: $status"
   if [[ "$status" == "$flag" ]]; then
       echo 'Idle process was terminated...'
       break
   else
       sleep 1
       timer=$(( $timer + 1 ))
       echo "waiting...$timer seconds"
   fi
   if [[ $timer == $timeout ]]; then
       echo "process was timeout after $timeout seconds"
   fi
done

}

run_timer
