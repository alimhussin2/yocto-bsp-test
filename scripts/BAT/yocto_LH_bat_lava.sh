#/bin/sh
# Yocto BAT script
# This test use lava-test-case wrapper script to parse pass and fail.

function tc_boot_first_boot ()
{
	dmesg > dmesg.log
}

function tc_generics_check_kernel_warning () {
	dmesg | grep -i warning | wc -l 
}

function tc_generics_check_kernel_version () {
	cat /proc/version
}

function tc_generics_kernel_cmdline () {
	cat /proc/cmdline
}

function tc_generics_partitions () {
	df |tee df.txt
}

function tc_generics_mount () {
	mount |tee mount.txt
}

function tc_generics_cpuinfo () {
	cat /proc/cpuinfo > cpuinfo.txt
}

function tc_wifi_driver_loaded() {
	dmesg |grep iwlwifi |grep loaded
}

function tc_wlan_enable() {
	phy=$(rfkill list |grep phy |cut -c 1,1)
	rfkill unblock $phy
	ifconfig wlan0 up
	iw wlan0 scan
}

function tc_bluetooth_enable() {
	hci=$(rfkill list |grep hci |cut -c 1,1)
	rfkill unblock $hci
	hciconfig up
}

# run tests
if [ $# = 1 ]
then
$1
else
	echo " running full BAT takes approximately 1.5 minutes
		firstboot
		check kernel version
		check cpu info
		check kernel cmdline
		partitions
		mounted file systems
		dmesg kernel warnings
		"
	echo
	echo

	tc_boot_first_boot
	ret=$?
	echo -n  ......first boot test...
	if [ $ret == 0 ]
	then
		echo PASS
		lava-test-case tc_boot_first_boot --result pass
	else
		echo FAILED!
		lava-test-case tc_boot_first_boot --result fail
	fi
	echo 
	echo 
	
	tc_generics_check_kernel_version
	ret=$?
        echo -n  ......kernel version test...
        if [ $ret == 0 ]
        then
                echo PASS
		lava-test-case tc_generics_check_kernel_version --result pass
        else
                echo FAILED!
		lava-test-case tc_generics_check_kernel_version --result fail
        fi
        echo 
        echo 

	tc_generics_cpuinfo
	ret=$?
        echo -n  ......cpuinfo test...
        if [ $ret == 0 ]
        then
                echo PASS
		lava-test-case tc_generics_cpuinfo --result pass
        else
                echo FAILED!
		lava-test-case tc_generics_cpuinfo --result fail
        fi
        echo 
        echo 


        tc_generics_kernel_cmdline
	ret=$?
	echo -n  ......check kernel cmdline test...
	if [ $ret == 0 ]
	then
		echo PASS
		lava-test-case tc_generics_kernel_cmdline --result pass
	else
		echo FAILED!
		lava-test-case tc_generics_kernel_cmdline --result fail
	fi
	echo
	echo
	tc_generics_partitions 
	ret=$?
	echo -n  ......check partition test...
	if [ $ret == 0 ]
	then
		echo PASS
		lava-test-case tc_generics_partitions --result pass
	else
		echo FAILED!
		lava-test-case tc_generics_partitions --result fail
	fi
	echo 
	echo
	tc_generics_mount 
	ret=$?
	echo -n  .........check mounts test...
	if [ $ret == 0 ]
	then
		echo PASS
		lava-test-case tc_generics_mount --result pass
	else
		echo FAILED!
		lava-test-case tc_generics_mount --result fail
	fi
	echo 
	echo
	tc_generics_check_kernel_warning
	ret=$?
	echo -n  .........check kernel warnings test...
	if [ $ret == 0 ]
	then
		echo PASS
		lava-test-case tc_generics_check_kernel_warning --result pass
	else
		echo FAILED!
		lava-test-case tc_generics_check_kernel_warning --result fail
	fi
fi

