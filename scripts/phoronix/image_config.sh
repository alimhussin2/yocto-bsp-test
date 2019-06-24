#!/bin/bash

devices=`ls /sys/block`
for device in $devices; do
    case $device in
        nvme*)
            echo mq-deadline > /sys/block/$device/queue/scheduler
	    echo "[ INFO ] Change IO scheduler for $device"
        ;;
        sd*)
	    echo mq-deadline > /sys/block/$device/queue/scheduler
	    echo "[ INFO ] Change IO scheduler for $device"
        ;;
    esac
done

