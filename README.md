# yocto-bsp-test
This repo contain example of codes for automated board support packages (BSP) tests on Yocto Project with LAVA. The tests include ptest, kselftest, Linux Test Project (LTP) and more. LAVA has a capability to deploy image such as Yocto Project on board, boot up and run the test.

## example-lava-job
These are some examples of LAVA jobs definition to boot the device using USB and network boot.
 - [USB boot] (example-lava-job/minnowboard-job-USB-boot.yaml)
 - [network boot] (example-lava-job/minnowboard-job-newtork-boot.yaml)

## Supported platform
Current we support Minnowboard-turbot which is x86 platform on LAVA. Device configuration for minnowboard is available [here] (../lava-config/dispatcher-config/device-types/minnowboard.jinja2)

## Author
 - Alim Hussin  

## References 
 - Yocto Project BSP test plan: https://wiki.yoctoproject.org/wiki/BSP_Test_Plan
 - Yocto Project repository: https://git.yoctoproject.org/cgit/cgit.cgi/poky/
 - Linaro LAVA: https://git.linaro.org/lava/lava.git/
