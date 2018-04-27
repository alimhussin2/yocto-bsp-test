#!/bin/bash -xe

# Description: Runtime test

TEST_ID=0
TEST_CASE="Nmae of testcase"
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


