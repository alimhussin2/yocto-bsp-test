from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.oeid import OETestID
from oeqa.core.decorator.data import skipIfNotDataVar

class MicrosdTest(OERuntimeTestCase):
    @classmethod
    def setUpClass(cls):
        cls.hw_test_path = '~/test'
        cls.microsd_path = os.path.join(cls.hw_test_path, 'microsd')
        cls.microsd_file = os.path.join(cls.microsd_path, 'hello_microsd')
        src = os.path.join(cls.tc.runtime_files_dir, 'bsp-test-helper')
        cls.tc.target.run('mkdir -p %s' % (cls.microsd_path))
        cls.tc.target.copyTo(src, '/usr/bin')

    @classmethod
    def tearDownClass(cls):
        cls.tc.target.run('rm -rf %s' % (cls.hw_test_path))

    @skipIfNotDataVar('HARDWARE_TEST','1',
            'Usb test only run on platform. It will skip on qemu.')
    @OETestID(241)
    def test_microsd_mount(self):
        command = ('bsp-test-helper --mount mmc %s' % (self.microsd_path))
        status, output = self.target.run(command)
        msg = ('Unable to mount MicroSD. '
                'Status and output:%s and %s.' %(status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['microsd.MicrosdTest.test_microsd_write_file'])
    @OETestID(242)
    def test_microsd_read_file(self):
        command = ('cat %s' % (self.microsd_file))
        status, output = self.target.run(command)
        msg = ('Unable to read MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['microsd.MicrosdTest.test_microsd_mount'])
    @OETestID(244)
    def test_microsd_write_file(self):
        command = ('echo hello_world > %s' % (self.microsd_file))
        status, output = self.target.run(command)
        msg = ('Unable to write to MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestDepends(['microsd.MicrosdTest.test_microsd_mount'])
    @OETestID(243)
    def test_microsd_unmount(self):
        command = ('bsp-test-helper --umount %s' % (self.microsd_path))
        status, output = self.target.run(command)
        msg = ('Unable to unmount MicroSD. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

