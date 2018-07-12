from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.oeid import OETestID
import subprocess

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
        self.assertEqual(status, 255, msg = None)
        command = 'lvl=$(runlevel | cut -d " " -f2); if [[ "$lvl" == "5" ]]; then exit 0; else exit 1; fi'
        status, output = self.target.run(command)
        msg = ('System did not start from runlevel 5. '
                'Status:%s.' % (status))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(198)
    def test_runlevel_3(self):
        status, output = self.target.run('init 3')
        msg = ('System unable to start with runlevel 3. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 255, msg = None)

        command = 'lvl=$(runlevel | cut -d " " -f2); if [[ $lvl == "3" ]]; then exit 0 ; else exit 1; fi'
        status, output = self.target.run(command)
        msg = ('Unable to change from runlevel 5 to 3. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

class BspHardwareTest(OERuntimeTestCase):

    @classmethod
    def setUpClass(cls):
        cls.tc.target.run('mkdir ~/test')

    @classmethod
    def tearDownClass(cls):
        cls.tc.target.run('rm -rf ~/test')

    @OETestID(216)
    def test_USB_mount(self):
        command = 'mkdir ~/test/stick; DEVICE=$(blkid | grep sd | cut -d ":" -f1 | sed -n 1p); mount $DEVICE ~/test/stick'
        status, output = self.target.run(command)
        msg = ('Unable to mount USB stick. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(217)
    @OETestDepends(['manualbsp.BspHardwareTest.test_USB_write_file'])
    def test_USB_read_file(self):
        command = 'ls -lah ~/test/stick/hello_stick'
        status, output = self.target.run(command)
        msg = ('Status and output:%s and %s.' % (status, output))
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
        command = 'umount ~/test/stick'
        status, output = self.target.run(command)
        msg = ('Unable to unmount USB stick. ' 
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(241)
    def test_MicroSD_mount(self):
        command = 'mkdir ~/test/microsd; DEVICE=$(blkid | grep mmcblk | cut -d ":" -f1 | sed -n 1p); mount $DEVICE ~/test/microsd'
        status, output = self.target.run(command)
        msg = ('Unable to mount MicroSD. '
                'Status and output:%s and %s.' %(status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['manualbsp.BspHardwareTest.test_MicroSD_mount'])
    @OETestID(242)
    def test_MicroSD_read_file(self):
        command = 'ls -lah ~/test/microsd'
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
        command = 'umount ~/test/microsd'
        status, output = self.target.run(command)
        msg = ('Unable to unmount MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    def test_copy_image_to_DUT(self):
        deploy_dir_image = self.tc.td['DEPLOY_DIR_IMAGE']
        image_link_name = self.tc.td['IMAGE_LINK_NAME']
        image = image_link_name + '.wic'
        wic_image = os.path.join(deploy_dir_image, image)
        wic_image = subprocess.check_output('ls -lah %s | cut -d " " -f12' % (wic_image), shell = True).decode("utf-8").strip('\n')
        src_img = os.path.join(deploy_dir_image, wic_image)
        dest_img = '/home/root/test'

       copy_image_status, output = self.target.copyTo(src_img, dest_img)
       msg = ('Image %s is not exist. '
                'Status and output:%s and %s.' % (image, copy_image_status, output))
        self.assertEqual(copy_image_status, 0, msg = msg)

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

