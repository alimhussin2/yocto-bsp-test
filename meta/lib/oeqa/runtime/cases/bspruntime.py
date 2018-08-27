from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.depends import OETestDepends
from oeqa.core.decorator.oeid import OETestID
import time

class BspRuntimeTest(OERuntimeTestCase):
    @classmethod
    def setUpClass(cls):
        src = os.path.join(cls.tc.runtime_files_dir, 'bsp-test-helper')
        cls.tc.target.copyTo(src, '/usr/bin')

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
        command = 'bsp-test-helper -r 5'
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
        command = 'bsp-test-helper -r 3'
        status, output = self.target.run(command)
        msg = ('Unable to change from runlevel 5 to 3. '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

    @OETestID(199)
    def test_xserver_start_with_runlevel_5(self):
        status, output = self.target.run('init 5')
        msg = ('Xserver unable to start with runlevel 5 '
                'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 255, msg = msg)
        time.sleep(2)
        command = 'bsp-test-helper -r 5'
        status, output = self.target.run(command)
        msg = ('Xserver cannot start on runlevel 5. '
                'Status:%s.' % (status))
        self.assertEqual(status, 0, msg = msg)

        status, output = self.target.run('bsp-test-helper --test-xorg')
        msg = ('Xserver not running. '
               'Status and output:%s and %s.' % (status, output))
        self.assertEqual(status, 0, msg = msg)

