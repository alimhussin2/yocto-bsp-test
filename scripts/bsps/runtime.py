#!/usr/bin/python3

import subprocess

class RuntimeTest():
    def __init__(self, testid = 0, className = 'bsps.RuntimeTests.'):
        self.testid = testid
        self.className = className

    def get_testid(self):
        return 'your testid %s' %(self.testid)

    def test_check_bash(self):
        '''
        TEST_ID: 240
        TEST_CASE: check if bash command exists with command "which bash"
        METHOD: 1. After system is up, check if bash command exists with command "which bash"
        EXPECTED_RESULTS: bash command should exist in image giving something as below 
                    "/bin/bash"
        '''
        self.testid = 240
        subprocess.call(['lava-test-case', '240:'+self.className+'test_check_bash', '--shell', 'which', 'bash'])

    def test_runlevel_5(self):
        '''
        TEST_ID: 228
        TEST_CASE: X server can start with runlevel 5
        METHOD: 1. boot up system with default runlevel
                2. type runlevel at command prompt
        EXPECTED_RESULTS: X server can start up well and desktop display has no problem .
                    output:N 5
        '''
        self.testid = 228
        subprocess.call(['lava-test-case', '228:'+self.className+'test_runlevel_5', '--shell', 'runlevel'])

    def test_runlevel_3(self):
        '''
        TEST_ID: 198
        TEST_CASE: 
        EXPECTED_RESULTS: system should boot to run level 3
        '''
        self.testid = 198
        subprocess.call(['lava-test-case', '198:'+self.className+'test_runlevel_3', '--shell', 'init 3'])

    def test_force_fail(self):
        self.testid = -99
        subprocess.call(['lava-test-case', '-99:'+self.className+'test_force_fail', '--shell', 'lava-test-raise "ERROR MESSGAE: This is error message in case test error"'])
        
t = RuntimeTest()
print(t.get_testid())
t.test_check_bash()
print(t.get_testid())
t.testid = 300
print(t.get_testid())
t.test_runlevel_5()
t.test_runlevel_3()
print(t.get_testid())
t.test_force_fail()
