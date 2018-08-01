#!/bin/bash

timeout=7200  # seconds

run_timer() {
local timer=0
file_minnow_done="$HOME/minnow.idle.done"
if [[ -f $file_minnow_done ]]; then
    rm $file_minnow_done
fi

while [[ $timer -lt $timeout ]];
do
   if [[ -f $file_minnow_done ]]; then
       echo 'Idle process has been terminated...'
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
