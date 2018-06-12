from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.oeid import OETestID
from oeqa.utils.commands import runCmd, bitbake

import os

class BspRuntimeTest(OERuntimeTestCase):

    @OETestID(240)
    def test_check_bash(self):
        status, output = self.target.run('which bash')
        msg = ('bash shell not working as expected. '
                'Status and output:%s and %s' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(198)
    def test_runlevel_3(self):
        status, output = self.target.run('init 3')
        msg = ('Unable to change from runlevel 5 to 3. '
                'Status and output:%s and %s' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(228)
    def test_runlevel_5(self):
        status, output = self.target.run('runlevel')
        msg = ('System did not start from runleve 5. '
                'Status and output:%s and %s' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    #@OETestID(210)
    #@OETestDepends(['bsp.BspToolsTest.test_rpm_dependency_install'])
    #def test_reboot(self):
    #    status, output = self.target.run('touch /home/root/minnow.idle.done')
    #    msg = ('System failed to reboot. '
    #            'Status and output:%s and %s' % (status, output))
    #    self.assertEqual(status, 0, msg = msg)

class BspHardwareTest(OERuntimeTestCase):

    #HOMEDIR = os.path.expanduser("~")
    '''
    Need to detect usb stick, hdd and microsd
    '''
    #def test_detect_peripheral(self):
    #    src = "/tmp/detect_device.sh"
    #    dest = "~/detect_device.sh"
    #   output = self.target.copyTo(src, dest)

    @OETestID(216)
    def test_USB_mount(self):
        status, output = self.target.run('mkdir ~/stick; DEVICE=$(blkid | grep sd | cut -d ":" -f1) && mount $DEVICE ~/stick')
        msg = ('Unable to mount USB stick. '
                'Status and output:%s and %s' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(217)
    @OETestDepends(['manualbsp.BspHardwareTest.test_USB_mount'])
    def test_USB_read_file(self):
        status, output = self.target.run('ls -lah  ~/stick/')
        msg = ('Status and output:%s and %s' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(219)
    #@OETestDepends(['manualbsp.HardwareTest.test_USB_read_file'])
    def test_USB_write_file(self):
        status, output = self.target.run('touch ~/stick/hello_stick')
        msg = ('Status and  output:%s and %s' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(218)
    #@OETestDepends(['manualbsp.HardwareTest.test_USB_read_file'])
    def test_USB_unmount(self):
        status, output = self.target.run('umount ~/stick')
        msg = ('Unable to unmount USB stick. ' 
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(241)
    def test_MicroSD_mount(self):
        status, output = self.target.run('mkdir microsd; DEVICE=$(blkid | grep mmc | cut -d ":" -f1); mount $DEVICE microsd')
        msg = ('Unable to mount MicroSD. '
                'Status and output:%s and %s.' %(status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(242)
    def test_MicroSD_read_file(self):
        status, output = self.target.run('ls -lah ~/microsd')
        msg = ('Unable to read MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(244)
    def test_MicroSD_write_file(self):
        status, output = self.target.run('touch ~/microsd/hello_mmc')
        msg = ('Unable to write to MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(243)
    def test_MicroSD_unmount(self):
        status, output = self.target.run('umount ~/microsd')
        msg = ('Unable to unmount MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

class BspToolsTest(OERuntimeTestCase):

    @OETestID(193)
    def test_rpm_dependency_install(self):
        '''
        steps
        1. bitbake mc
        2. copy file mc.rpm to target
        3. install mc in target $ rpm -ivh mc.rpm
        '''
        src = "/tmp/mc-4.8.20-r0.corei7_64.rpm"
        dst = "/tmp/mc-4.8.20-r0.corei7_64.rpm"
        rpm_file = "/tmp/mc-4.8.20-r0.corei7_64.rpm"
        #homedir = os.path.expanduser("~")
        #bitbake('mc')
        status, output = self.target.copyTo(src, dst)
        msg = 'File could not be copied. Output: %s' % output
        self.assertEqual(status, 0, msg = msg)
        status, output = self.target.run('rpm -ivh %s' % (rpm_file))
        msg = ('Status and output:%s and %s' % (status, output))
        self.assertEqual(status, 1, msg = msg)
