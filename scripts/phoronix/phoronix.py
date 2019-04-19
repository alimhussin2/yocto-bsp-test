#!/usr/bin/python3

# This is a wrapper script to configure, run and upload results of phoronix test suite.
# Phoronix test suite run benchmark for a batch test suite.

import os
import subprocess
import argparse
import datetime
import re
import fnmatch
import ntpath
import xml.etree.ElementTree as ET
import sys
from os import environ
from ptsxml2json import convert_xmltojson
try:
    utilsdir = os.path.abspath(os.path.dirname('__file__'))
    utilsdir = os.path.join(ntpath.split(utilsdir)[0], 'utils')
    sys.path.append(utilsdir)
    from create_archives import *
    from basic_config import *
    from board_info import update_board_info
except Exception as e:
    print('ERROR: %s in %s' % (e, utilsdir))

def check_pkg():
    output = subprocess.run(['which', 'phoronix-test-suite'])
    if output.returncode == 1:
        print("ERROR: phoronix-test-suite not install")
        exit()

def get_boardinfo():
    with open('/sys/class/dmi/id/board_name', 'r') as f:
        board_name = f.read().replace('\n', '').replace(' ', '_')
    return board_name

def get_os():
    os_name = []
    with open('/etc/os-release') as f:
        os = re.findall(r'ID=.*', f.read())
    for i in os:
        os_name.append(re.sub('[^a-zA-Z0-9.\-]+', '', i).replace('ID',''))
    return os_name[0] + '-' + os_name[1]
    

def run_tests(tests_file):
    testsuites = ""
    if os.path.abspath(tests_file):
        with open(tests_file, 'r') as list_tests:
            for test in list_tests:
                testsuites += test.replace('\n', ' ')
        print("INFO: The following test suites will executed: %s" % testsuites)
        cmd = 'export DISPLAY=:0; phoronix-test-suite batch-benchmark %s' % testsuites
        subprocess.run(cmd, shell=True)
    else:
        print("ERROR: Test cases is not defined. Please create a file testcases.txt with contain a list of testcases.")

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
        item.find('ResultsDirectory').text = os.path.join(results_dir, get_boardinfo())
    print("INFO: save phoronix config to %s" % (os.path.join("/etc", phoronix_config)))
    tree.write(os.path.join("/etc", phoronix_config))

def get_resultsdir():
    tree = ET.parse('/etc/phoronix-test-suite.xml')
    root = tree.getroot()
    resultsdir = ''
    lresultsdir = []
    for n in root.iter('Testing'):
        resultsdir = n.find('ResultsDirectory').text
    date = datetime.now().strftime("%Y-%m-%d")
    lfiles = os.listdir(resultsdir)
    for f in lfiles:
        if fnmatch.fnmatch(f, date + '*'):
            lresultsdir.append(os.path.join(resultsdir, f))
    return lresultsdir

def get_resultsfiles(resultsdir):
    head, lresultsdir = ntpath.split(resultsdir)     
    return lresultsdir

def convert_json():
    cmd = 'phoronix-test-suite show-result'
    output = subprocess.check_output(cmd, shell=True)
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    results = re.findall(re.escape(date) + r'.*[0-9]', output.decode())
    for r in range(len(results)):
        cmd = 'phoronix-test-suite result-file-to-json %s' % results[r]
        results_json =  results[r] + ".json"
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p, open(results_json, "w+") as f:
            for line in p.stdout:
                f.write(line.decode())
                f.flush()
            f.close()
        print("INFO: Saved result in %s" % results_json)

def compare_results(current_results, results_dir):
    if os.path.exists(results_dir):
        subprocess.call(['phoronix-test-suite merge-results %s %s'] % (current_results, results_dir), shell=True)
    else:
        print("ERROR: Unable to compare results as % is not exists." % results_dir)

def publish_results(results, upload_server):
    os_name = get_os()
    suffix_path = get_boardinfo() + '/' + os_name
    upload_server = os.path.join(upload_server, suffix_path)
    if not os.path.exists(upload_server):
        os.mkdir(upload_server)
    for r in results:
        cmd = "cp -r %s %s" % (r, upload_server)
        output = subprocess.check_output(cmd, shell=True).decode()
        print("INFO: Successfully upload to %s" % os.path.join(upload_server, get_resultsfiles(r)))

def auto_publish_results(results):
    ww_dir = create_archives_by_daily(None, True)
    base_dir = os.path.join(ww_dir, 'lava')
    upload_dir = base_dir
    lava_dirs = get_lava_dir()
    phoronixResultsDir = []
    for lava_dir in lava_dirs:
        phoronix_dir = 'phoronix-test-suite'
        suffix_path = get_boardinfo() + '/' + get_os()
        upload_dir = os.path.join(upload_dir, lava_dir)
        upload_dir = os.path.join(upload_dir, phoronix_dir)
        upload_dir = os.path.join(upload_dir, suffix_path)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    for result in results:
        dest_dir = os.path.join(upload_dir, get_resultsfiles(result))
        cmd = 'cp -r %s %s' % (result, upload_dir)
        subprocess.check_output(cmd, shell=True).decode()
        print('INFO: Successfully upload to %s' % dest_dir)
        phoronixResultsDir.append(dest_dir)
    data = {"phoronixResults" : phoronixResultsDir}
    for lava_dir in lava_dirs:
        b_info = os.path.join(base_dir, lava_dir) + '/board_info.json'
        if os.path.isfile(b_info):
            print('INFO: Successfully updated %s' % b_info)
            update_board_info(os.path.join(base_dir, lava_dir), data)
        else:
            print('ERROR: Unable to update %s. File is missing.' % b_info)

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
    parser.add_argument("--convert-json", action="store_true", help="convert phoronix test results to json format")
    parser.add_argument("--nfs-mount", help="do nfs mount by providing argument as nfsserver, src, dest", nargs = '*')
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
    convert_json = args.convert_json
    nfs_mount = args.nfs_mount

    check_pkg()
    #check phoronix configuration file
    if not os.path.isfile(os.path.join("/etc","phoronix-test-suite.xml")):
        print("Warning: Phoronix configuration file is not exist!\n"
              "Create a new configuration by passing arguments \n"
              "installed-test, cache-directory, proxy-address, \n"
              "proxy-port, results-directory")
        if all(var is None for var in [results_dir, installed_tests, cache_dir, proxy_address, proxy_port]):
            print("ERROR: some arguments e.g. results-storage, installed-tests, cache-directory, \n"
                  "proxy-address or proxy-port are not set.")
            exit()
        else:
            print("INFO: Configuring phoronix")
            #print("Info: proxy address %s, proxy port %s, installed_tests %s, cache_dir %s, results_dir %s"
            #        % (proxy_address, proxy_port, installed_tests, cache_dir, results_dir))
            configure_phoronix(proxy_address, proxy_port, installed_tests, cache_dir, results_dir)
    if start_tests:
        run_tests(start_tests)
        if nfs_mount:
            nfs_server = args.nfs_mount[0]
            nfs_src = args.nfs_mount[1]
            nfs_dest = args.nfs_mount[2]
            do_mountnfs(nfs_server, nfs_src, nfs_dest)
        auto_publish_results(get_resultsdir())
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
        print("INFO: The test results will upload to server %s" % upload_server)
        publish_results(get_resultsdir(), upload_server)
    if convert_json:
        print("INFO: Convert phoronix test results to json format")
        lresultdirs = get_resultsdir()
        for resultdir in lresultdirs:
            result = os.path.join(resultdir, 'composite.xml')
            if os.path.isfile(result):
                convert_xmltojson(result)
            else:
                print('ERROR: %s is not exist!' % result)
