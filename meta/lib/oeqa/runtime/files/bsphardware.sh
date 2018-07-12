#!/bin/bash

# Description: This script used for Yocto Project BSP test.
#              manualbsp.py script is depend on this script
#              that available in poky/meta/lib/oeqa/runtime/cases/manualbsp.py.
#              This script is should be located in
#              poky/meta/lib/oeqa/runtime/cases/

usage() {
echo "BSP hardware test is a script used to test hardware"
echo "such as USB stick, micro SD and SSD hard disk on Yocto Project."
echo ""
echo "Usage:"
echo "-d, --device <keyword, e.g. sd/mmc         Get device's name"
echo "-p, --partition <partition's number>       Get device's partitions"
echo "-sp, --setPartition <partition's number>   Set partition's number "
echo "-m, --mount <path/to/mount>                Mount the device to /path/to/mount"
echo "-u, --umount <path/to/unmount>             Unmont the mounted device"
echo "-f, --format [-d <device>]                 Format the device"
echo "-F, --flash <filename>                     Flash device with image"
echo "-t, --touch <filename>                     Create a file"
echo "-r, --runlevel <3|5>                       Get runlevel on current system"
echo "-h, --help                                 Show the usage"
}

options() {
SETPARTITION=""
DEVICE=""
while [[ $# -gt 0 ]]; do
case "$1" in
    -d|--device)
        echo "get device's name"
        DEVICE=$(blkid | grep $2 | cut -d ":" -f1 | sed -n 1p | sed "s/[0-9]//g")
        echo $DEVICE
        ;;
    -p|--partition)
        echo "get device's partition $2"
        PARTITION=$(blkid | grep $DEVICE | cut -d ":" -f1 | grep $2)
        echo $PARTITION
        ;;
    -sp| --setPartition)
         echo "Set partition: $2"
         SETPARTITION=$2
         ;;
    -F|--flash)
        if [[ "$2" == "" ]]; then
            echo "[ERROR]: Missing filename."
            exit 1
        fi
        file=$(find . -name $2)
        if [[ "$DEVICE" != "" ]]; then
            if [[ -f $file ]]; then
                echo dd if=$file of=$DEVICE status=progress
            else
                echo "[ERROR]: File $file not exist! Unable to flash $DEVICE."
                exit 1
            fi
        else
           echo "[ERROR]: Target device to flash is not define."
           exit 1
        fi
        ;;
    -t|touch)
        if [[ -f $2 ]]; then
            echo "create a file: $2"
            touch $2
        else
            echo "[Error]: File $2 already created!"
            exit 1
        fi
        ;;
    -m|mount)
        if [[ ! -d $2 ]];then
            mkdir $2
        fi
        if [[ "$DEVICE" == "" || " $SETPARTITION" == "" ]]; then
            echo "[ERROR]: Target device and partition not found." 
            echo "Use -d <device_keyword> -sp <partition's number> -m <dir>"
            exit 1
        else
            echo "Mounting removable media..."
            echo "mount $DEVICE$SETPARTITION $2"
            mount $DEVICE$SETPARTITION $2
            exit 
        fi
        ;;
    -u|umount)
        echo "Unmount $2"
        if [[ -d $2 ]]; then
            echo umount $2
            umount $2
        else
            echo "[Error]: No mount point on $2"
            exit 1
        fi
        if [[ $? -eq 0 ]];then 
            echo "Device $2 unmount successfully"
            echo "rm -rf $2"
            rm -rf $2
        fi
        ;;
    -r|--runlevel)
        level=$(runlevel | grep $2 | cut -d " " -f2)
        echo "[DEBUG]: $level"
        if [[ "$2" == "3" || "$2" == "5" ]]; then
            if [[ "$level" == "3" ]]; then
                echo "[INFO]: System start with runlevel $level"
                exit 0
            elif [[ "$level" == "5" ]]; then
                echo "[INFO]: System start with runlevel $level"
                exit 0
            else
                echo "[INFO]: System did not start with runlevel $2"
                exit 1
            fi
        else
            echo "[ERROR]: Runlevel other than 3 & 5 are not allowed."
            exit 1
        fi
        ;;
    -h|--help)
        usage
        exit 0
        ;;
    *) 
        echo "[Error]: Arguments $1 is not exists." 
        usage
        exit 1
        ;;
esac
shift
shift
done
}

main() {

if [ "$#" == "0" ];then
    usage
    exit 1
else
    options "${POSITIONAL[@]}"
fi
}

POSITIONAL=()
POSITIONAL+=("$@")
echo DEBUG: arguments: ${POSITIONAL[*]}
main ${POSITIONAL[@]}