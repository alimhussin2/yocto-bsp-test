#!/usr/bin/python3

import  os.path
from lavaTest import LavaTest

class ToolsTest():
    def test_rpm_install():
        testid = '193'
        testCaseName = 'test_rpm_install_dependency'
        path = '/home/root/'
        rpm_file = 'mc-4.8.20-r0.corei7_64.rpm'
        f = LavaTest('ToolsTest.')
        if (os.path.isfile(path + rpm_file) == True):
            print('file %s is exist!' % (rpm_file))
            #f.run_test(testid, testCaseName, 'rpm -ivh ' + rpm_file)
            expected_output = 'error: Failed dependencies:'
            output = f.get_stderr(testid, testCaseName, 'rpm -ivh ' + rpm_file)
            print(output)
            if (expected_output == output):      
                f.set_testPass(testid, testCaseName)
        else:                                    
            print('file %s is not exist' % (rpm_file))
            #f.set_testFail(testid, testCaseName)
            output = f.get_stderr(testid, testCaseName, 'rpm -ivh ' + rpm_file)
            print(output)
                             
ToolsTest.test_rpm_install()
t = LavaTest('bsps.RuntimeTest.')
t.get_testid()
t.get_testClass()
t.run_test('240', 'test_check_bash', 'which bash')
t.run_test('198', 'test_runlevel_3', 'init 3')
t.run_test('228', 'test_runlevel_5', 'runlevel')
t.get_testid()
t.run_test('-99', 'test_whoami', 'whoami')
t.run_test('-99', 'test_kernel_version', 'uname -a')


y = LavaTest('bsps.ToolsTest.')
y.get_testid()
y.get_testClass()
y.run_test('198', 'test_runlevel_3', 'init 3')
y.get_testid()
