from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.oeid import OETestID
import subprocess
import time

class BspRuntimeTest(OERuntimeTestCase):

    @OETestID(240)
    def test_check_bash(self):
        status, output = self.target.run('which bash')
        msg = ('bash shell not working as expected. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(228)
    def test_runlevel_5(self):
        status, output = self.target.run('init 5')
        msg = ('System unable to init 5 '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 255, msg = msg)
        time.sleep(2)
        #command = 'lvl=$(runlevel | cut -d " " -f2); if [[ $lvl == "5" ]]; then exit 0; else exit 1; fi'
        command = 'bsphardware -r 5'
        status, output = self.target.run(command)
        msg = ('System did not start from runlevel 5. '
                'Status:%s.' % (status))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(198)
    def test_runlevel_3(self):
        status, output = self.target.run('init 3')
        msg = ('System unable to start with runlevel 3. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 255, msg = msg)
        time.sleep(2)
        #command = 'lvl=$(runlevel | cut -d " " -f2); if [[ $lvl == "3" ]]; then exit 0 ; else exit 1; fi'
        command = 'bsphardware -r 3'
        status, output = self.target.run(command)
        msg = ('Unable to change from runlevel 5 to 3. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

class BspHardwareTest(OERuntimeTestCase):

    @classmethod
    def setUpClass(cls):
        src = os.path.join(cls.tc.runtime_files_dir, 'bsphardware')
        cls.tc.target.run('mkdir ~/test')
        cls.tc.target.copyTo(src, '/usr/bin')

    @classmethod
    def tearDownClass(cls):
        cls.tc.target.run('echo done')
        #cls.tc.target.run('rm -rf ~/test')
        #cls.tc.target.run('rm -rf /usr/bin/bsphardware')
        #cls.tc.target.copyFrom('~/bsphardware.log', '/tmp/bsphardware.log')

    @OETestID(216)
    def test_USB_mount(self):
        #command = 'mkdir ~/test/stick; DEVICE=$(blkid | grep sd | cut -d ":" -f1 | sed -n 1p); mount $DEVICE ~/test/stick'
        command = 'bsphardware -d sd -sp 1 -m ~/test/stick'
        status, output = self.target.run(command)
        msg = ('Unable to mount USB stick. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(217)
    @OETestDepends(['manualbsp.BspHardwareTest.test_USB_write_file'])
    def test_USB_read_file(self):
        command = 'cat ~/test/stick/hello_stick'
        status, output = self.target.run(command)
        msg = ('Unable to read file from USB stick. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['manualbsp.BspHardwareTest.test_USB_mount'])
    @OETestID(219)
    def test_USB_write_file(self):
        command = 'touch ~/test/stick/hello_stick'
        status, output = self.target.run(command)
        msg = ('Status and  output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['manualbsp.BspHardwareTest.test_USB_mount'])
    @OETestID(218)
    def test_USB_unmount(self):
        #command = 'umount ~/test/stick'
        command = 'bsphardware -u ~/test/stick'
        status, output = self.target.run(command)
        msg = ('Unable to unmount USB stick. ' 
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(241)
    def test_MicroSD_mount(self):
        #command = 'mkdir ~/test/microsd; DEVICE=$(blkid | grep mmcblk | cut -d ":" -f1 | sed -n 1p); mount $DEVICE ~/test/microsd'
        command = 'bsphardware -d mmc -sp p1 -m ~/test/microsd'
        status, output = self.target.run(command)
        msg = ('Unable to mount MicroSD. '
                'Status and output:%s and %s.' %(status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['manualbsp.BspHardwareTest.test_MicroSD_write_file'])
    @OETestID(242)
    def test_MicroSD_read_file(self):
        command = 'cat ~/test/microsd/hello_mmc'
        status, output = self.target.run(command)
        msg = ('Unable to read MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['manualbsp.BspHardwareTest.test_MicroSD_mount'])
    @OETestID(244)
    def test_MicroSD_write_file(self):
        command = 'touch ~/test/microsd/hello_mmc'
        status, output = self.target.run(command)
        msg = ('Unable to write to MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['manualbsp.BspHardwareTest.test_MicroSD_mount'])
    @OETestID(243)
    def test_MicroSD_unmount(self):
        #command = 'umount ~/test/microsd'
        command = 'bsphardware -u ~/test/microsd'
        status, output = self.target.run(command)
        msg = ('Unable to unmount MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    #def test_copy_image_to_DUT(self):
    #    deploy_dir_image = self.tc.td['DEPLOY_DIR_IMAGE']
    #    image_link_name = self.tc.td['IMAGE_LINK_NAME']
    #    image = image_link_name + '.wic'
    #    wic_image = os.path.join(deploy_dir_image, image)
    #    wic_image = subprocess.check_output('ls -lah %s | cut -d " " -f12' % (wic_image), shell = True).decode("utf-8").strip('\n')
    #    src_img = os.path.join(deploy_dir_image, wic_image)
    #    dest_img = '/home/root/test'

    #    copy_image_status, output = self.target.copyTo(src_img, dest_img)
    #    msg = ('Image %s is not exist. '
    #            'Status and output:%s and %s.' % (image, copy_image_status, output))
    #    self.assertEqual(copy_image_status, 0, msg = msg)

    #@OETestDepends(['manualbsp.BspHardwareTest.test_copy_image_to_DUT'])
    #def test_prepare_image_MicroSD(self):
    #    command_format_microsd = 'DEVICE=$(blkid | grep mmcblk | cut -d ":" -f1 | sed -n 1p); mkfs.ext4 $DEVICE'
    #    status, output = self.target.run(command_format_microsd)
    #    msg = ('Unable to format MicroSD. '
    #            'Status and output:%s and %s.' % (status, output))
    #    self.assertEqual(status, 0, msg = msg)

    #@OETestDepends(['manualbsp.BspHardwareTest.test_copy_image_to_DUT'])
    #def test_prepare_image_USB_stick(self):
    #    command_format_microsd = 'DEVICE=$(blkid | grep sd | cut -d ":" -f1 | sed -n 1p); mkfs.ext4 $DEVICE'
    #    status, output = self.target.run(command_format_microsd)
    #    msg = ('Unable to format USB stick. '
    #            'Status and output:%s and %s.' % (status, output))
    #    self.assertEqual(status, 0, msg = msg)

