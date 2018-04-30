#!/bin/bash -xe

# Description: Runtime test

TEST_ID=0
TEST_CASE="Name of testcase"
CMD="shell command"

# TEST_ID: 228
# TEST_CASE: X server can start with runlevel 5
# METHOD: 1. boot up system with default runlevel
#         2. type runlevel at command prompt
# EXPECTED_RESULTS: X server can start up well and desktop display has no problem .
#                   output:N 5
TEST_ID=228
TEST_CASE="X server can start with runlevel 5"
CMD="runlevel"
echo $TEST_ID": "$TEST_CASE
lava-test-case $TEST_ID-runlevel-5 --shell $CMD
#lava-test-case [228]-runlevel-5 --shell runlevel

# TEST_ID: 240
# TEST_CASE: check if bash command exists with command "which bash"
# METHOD: 1. After system is up, check if bash command exists with command "which bash"
# EXPECTED_RESULTS: bash command should exist in image giving something as below 
#                   "/bin/bash"
TEST_ID=240
TEST_CASE="check bash"
CMD="which bash"
lava-test-case $TEST_ID-check-bash --shell $CMD

# TEST_ID=198
# TEST_CASE: boot from runlevel 3
# METHOD: 1. Boot into system and edit /etc/inittab to make sure that system enter at the run level 3 by default, this is done by changing the line 
#            id:5:initdefault -> id:3:initdefault
#         2. Reboot system, and press "Tab" to enter "grub"
#         3. Get into the "kernel" line with the edit option  "e" and add "psplash=false text" at the end line.
#         4. Press "F10" or "ctrl+x" to boot system
#         5. If system ask you for a login type "root"
# EXPECTED_RESULTS: System should boot to run level 3, showing the command prompt.
TEST_ID=198
TEST_CASE="switch to runlevel 3"
CMD="init 3"
lava-test-case $TEST_ID-switch-runlevel-3 --shell $CMD

TEST_ID=1981
TEST_CASE="runlevel 3"
CMD="runlevel"
lava-test-case $TEST_ID-runlevel-3 --shell $CMD

TEST_ID=1980
TEST_CASE="switch to runlevel 5 from runlevel 3"
CMD="init 5"
lava-test-case $TEST_ID-runlevel-3-to-5 --shell $CMD

# TEST_ID=210
# TEST_CASE: reboot system
# METHOD: run 'reboot' command in terminal
TEST_ID=210
TEST_CASE="reboot system"
CMD="reboot"
lava-test-case $TEST_ID-reboot-system --shell $CMD
