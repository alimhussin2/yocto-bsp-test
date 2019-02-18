#!/usr/bin/python3

# This is a wrapper script to configure, run and upload results of phoronix test suite.
# Phoronix test suite run benchmark for a batch test suite.

import os
import subprocess
import argparse
from shutil import copyfile
import xml.etree.ElementTree as ET

def check_pkg():
    output = subprocess.run(['which', 'phoronix-test-suite'])
    if output.returncode == 1:
        print("Error: phoronix-test-suite not install")
        exit()

def run_tests(tests_file):
    testsuites = ""
    if os.path.abspath(tests_file):
        with open(tests_file, 'r') as list_tests:
            for test in list_tests:
                testsuites += test.replace('\n', ' ')
        print("Info: The following test suites will executed: %s" % testsuites)
        subprocess.Popen(['export DISPLAY=:0; phoronix-test-suite batch-benchmark %s' % testsuites], shell=True)
    else:
        print("Error: Test cases is not defined. Please create a file testcases.txt with contain a list of testcases.")

def configure_phoronix(proxy_address, proxy_port, installed_dir, cache_dir, results_dir):
    # configure proxy, installation path and results storage
    phoronix_config = "phoronix-test-suite.xml"
    tree = ET.parse(os.path.abspath('template/phoronix-test-suite.xml'))
    root = tree.getroot()
    for item in root.iter('Networking'):
        item.find('ProxyAddress').text = proxy_address
        item.find('ProxyPort').text = proxy_port
    for item in root.iter('Installation'):
        item.find('EnvironmentDirectory').text = installed_dir
        item.find('CacheDirectory').text = cache_dir
    for item in root.iter('Testing'):
        item.find('ResultsDirectory').text = results_dir
    print("save phoronix config to %s" % (os.path.join("/etc", phoronix_config)))
    tree.write(os.path.join("/etc", phoronix_config))

def compare_results(current_results, results_dir):
    if os.path.exists(results_dir):
        subprocess.call(['phoronix-test-suite merge-results %s %s'] % (current_results, results_dir), shell=True)
    else:
        print("Error: Unable to compare results as % is not exists." % results_dir)

def publish_results(results, upload_server):
    cmd = ("curl -F 'path=@%s' %s" % (results, upload_server))
    output = subprocess.check_output(cmd, shell=True).decode()
    if output.returncode == 0:
        print("Successfully upload to %s" % output)

def register_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-storage", help="path to store test results")
    parser.add_argument("--installed-tests", help="path to store installed tests")
    parser.add_argument("--compare-results", help="Compare results with others run or other platfrom", nargs = '*')
    parser.add_argument("--run-tests", help="run phoronix test suite with predefined test suites")
    parser.add_argument("--upload-results", help="upload test results to artifactorial")
    parser.add_argument("--cache-directory", help="path to store cache files")
    parser.add_argument("--proxy-address", help="Hostname of proxy server. e.g proxy.com")
    parser.add_argument("--proxy-port", help="port number of proxy server")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = register_arguments()
    results_dir = args.results_storage
    installed_tests = args.installed_tests
    upload_server = args.upload_results
    compare_results = args.compare_results
    start_tests = args.run_tests
    cache_dir = args.cache_directory
    proxy_address = args.proxy_address
    proxy_port = args.proxy_port

    check_pkg()
    # check phoronix configuration file
    if not os.path.isfile(os.path.join("/etc","phoronix-test-suite.xml")):
        print("Warning: Phoronix configuration file is not exist!\n"
              "Create a new configuration by passing arguments"
              "installed-test, cache-directory, proxy-address,"
              "proxy-port, results-directory")
        if all(var is None for var in [results_dir, installed_tests, cache_dir, proxy_address, proxy_port]):
            print("Error: some arguments e.g. results-storage, installed-tests, cache-directory, \n"
                  "proxy-address or proxy-port are not set.")
            exit()
        else:
            print("Info: Configure phoronix with these variable")
            print("Info: proxy address %s, proxy port %s, installed_tests %s, cache_dir %s, results_dir %s"
                    % (proxy_address, proxy_port, installed_tests, cache_dir, results_dir))
            configure_phoronix(proxy_address, proxy_port, installed_tests, cache_dir, results_dir)
    if start_tests:
        run_tests(start_tests)
    if compare_results:
        results1 = args.compare_results[0]
        results2 = args.compare_results[1]
        if all(var is None for var in [results1, results2]):
            print("Error: To compare results, use --compare-results results1 results2")
            exit()
        else:
            print("Comparing results %s with %s" % (results1, results2))
            compare_results(results1, results2)
    if upload_server:
        print("The test results will upload to server %s" % upload_server)
        #publish_results(results_dir, upload_server)

