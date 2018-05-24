#!/usr/bin/python3

import subprocess

class LavaTest():
    def __init__(self, className = 'bsps.'):
        testid =0
        self.testid = testid
        self.className = className

    def get_testid(self):
        print('test id = %s' %(self.testid))

    def get_testClass(self):
        print('test class name = %s' % (self.className))

    def set_testPass(self, testid, testCaseName):
        self.testid = testid
        subprocess.call(['lava-test-case', testid + ':' + self.className + testCaseName, '--result', 'pass'])

    def set_testFail(self, testid, testCaseName):
        self.testid = testid
        subprocess.call(['lava-test-case', testid + ':' + self.className + testCaseName, '--result', 'fail'])

    def get_stderr(self, testid, testCaseName, command):
        process = subprocess.Popen(['lava-test-case', testid + ':' + self.className + testCaseName, '--shell', command], stderr=subprocess.PIPE)
        return process.communicate()
        

    def run_test(self, testid, testCaseName, command):
        self.testid = testid
        subprocess.call(['lava-test-case', testid + ':' + self.className + testCaseName, '--shell', command]) 


#rpm_file = 'mc.rpm'
#f = LavaTest('test.bsptest.')
#output = f.get_stderr('1', 'check_file', 'rpm -ivh ' + rpm_file)
#print(output)

'''
t = LavaTest(0, 'bsps.RuntimeTest.')
t.get_testid()
t.get_testClass()
t.run_test('240', 'test_check_bash', 'which bash')
t.run_test('198', 'test_runlevel_3', 'init 3')
t.run_test('228', 'test_runlevel_5', 'runlevel')
t.get_testid()
t.run_test('-99', 'test_whoami', 'whoami')
t.run_test('-99', 'test_kernel_version', 'uname -a')


y = LavaTest(20, 'bsps.ToolsTest.')
y.get_testid()
y.get_testClass()
y.run_test('198', 'test_runlevel_3', 'init 3')
y.get_testid()
'''


