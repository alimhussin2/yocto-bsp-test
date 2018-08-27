from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.oeid import OETestID
from oeqa.core.decorator.data import skipIfNotDataVar

class USBTest(OERuntimeTestCase):
    @classmethod
    def setUpClass(cls):
        cls.hw_test_path = '~/test'
        cls.usb_path = os.path.join(cls.hw_test_path, 'stick')
        cls.usb_file = os.path.join(cls.usb_path, 'hello_stick')
        src = os.path.join(cls.tc.runtime_files_dir, 'bsp-test-helper')
        cls.tc.target.run('mkdir -p %s' % (cls.usb_path))
        cls.tc.target.copyTo(src, '/usr/bin')

    @classmethod
    def tearDownClass(cls):
        cls.tc.target.run('rm -rf %s' % (cls.hw_test_path))

    @skipIfNotDataVar('HARDWARE_TEST','1',
            'Usb test only run on platform. It will skip on qemu.')
    @OETestID(216)
    def test_usb_mount(self):
        command = ('bsp-test-helper --mount pendrive %s' % (self.usb_path))
        status, output = self.target.run(command)
        msg = ('Unable to mount USB stick. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(217)
    @OETestDepends(['usb.USBTest.test_usb_write_file'])
    def test_usb_read_file(self):
        command = ('cat %s' % (self.usb_file))
        status, output = self.target.run(command)
        msg = ('Unable to read file from USB stick. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['usb.USBTest.test_usb_mount'])
    @OETestID(219)
    def test_usb_write_file(self):
        command = ('echo hello_world > %s' % (self.usb_file))
        status, output = self.target.run(command)
        msg = ('Status and  output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['usb.USBTest.test_usb_mount'])
    @OETestID(218)
    def test_usb_unmount(self):
        command = ('bsp-test-helper --umount %s' % (self.usb_path))
        status, output = self.target.run(command)
        msg = ('Unable to unmount USB stick. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)
