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
import shutil
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
    for rd in os.listdir(resultsdir):
        b = os.path.join(resultsdir, rd)
        if os.path.isdir(b):
            lresultsdir.append(b)
    latest_result = max(lresultsdir, key=os.path.getmtime)
    return latest_result

def get_resultsfiles(resultsdir):
    head, lresultsdir = ntpath.split(resultsdir)     
    return lresultsdir

def get_dir(option):
    """
    File structure is like this
    <base_dir>/<ww_dir>/<lava_dir>/<lava_id_dir>/<phoronix_dir>/<machine_dir>/<os_release_dir>/<pts_results_dir>
    e.g. of full phoronix file structure
    /srv/data/archives/2019/5/19/19.2/lava/lava-2236/phoronix-test-suite/NUC6i7KYB/poky-2.7-snapshot-20190424/2019-05-07-0633/
    <base_dir> /srv/data
    <ww_dir> /srv/data/2019/5/19/19.2
    <lava_dir> /srv/data/2019/5/19/19.2/lava
    <lava_id_dr> /srv/data/2019/5/19/19.2/lava/lava-2236
    <phoronix_dir> /srv/data/2019/5/19/19.2/lava/lava-2236/phoronix-test-suite
    <machine_dir> /srv/data/2019/5/19/19.2/lava/lava-2236/phoronix-test-suite/NUC6i7KYB
    <os_release_dir> /srv/data/2019/5/19/19.2/lava/lava-2236/phoronix-test-suite/NUC6i7KYB/poky-2.7-snapshot-20190424

    """
    lava_dir = ""
    lava_id = ""
    lava_idx = []
    count = 0
    for d in get_lava_dir():
        lava_idx.append(os.path.join('/', d))
    lava_id = max(lava_idx, key=os.path.getmtime).replace('/', '')
    base_dir = "/srv/data/archives"
    for r, d, f in os.walk(base_dir):
        for ww in d:
            if re.findall(lava_id, ww):
                lava_dir = r
                ww_dir =lava_dir.replace('/lava', '')
            else:
                count += 1
        if count == len(d):
            ww_dir = create_archives_by_daily(None, True)
            lava_dir = os.path.join(ww_dir, 'lava')
    lava_id_dir = os.path.join(lava_dir, lava_id)
    phoronix_dir = os.path.join(lava_id_dir, 'phoronix-test-suite')
    machine_dir = os.path.join(phoronix_dir, get_boardinfo())
    os_release_dir = os.path.join(machine_dir, get_os())
    if option == "ww_dir":
        return ww_dir
    if option == "lava_dir":
        return lava_dir
    if option == "lava_id_dir":
        return lava_id_dir
    if option == "phoronix_dir":
        return phoronix_dir
    if option == "machine_dir":
        return machine_dir
    if option == "os_release_dir":
        return os_release_dir

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

def auto_compare_results(results_dir, machine1, machine2, os1, os2, upload_dir):
    """
    This function is meant to compare previous results from archives
    by query by machines and OS then do the comparison.
    """
    list_results = []
    if (machine1 == machine2) and (os1 == os2):
        print("ERROR: Cannot compare same OS on same machine")
        exit()
    for r, d, f in os.walk(results_dir):
        for file in f:
            if '.xml' in file:
                list_results.append(os.path.join(r, file))
    results1 = query_results(list_results, machine1, os1)
    results2 = query_results(list_results, machine2, os2)
    print("INFO: Result1 %s" % results1)
    print("INFO: Result2 %s" % results2)
    tmp_results_dir = "/tmp/merge-results"
    modify_config(tmp_results_dir)
    t_results1 = get_resultsfiles(results1)
    t_results2 = get_resultsfiles(results2)
    shutil.copytree(results1, os.path.join(tmp_results_dir, t_results1))
    shutil.copytree(results2, os.path.join(tmp_results_dir, t_results2))
    cmd = "phoronix-test-suite merge-results %s %s" % (t_results1, t_results2)
    subprocess.run(cmd, shell=True)
    for m in os.listdir(tmp_results_dir):
        if re.findall(r'merge-*', m):
            shutil.copytree(os.path.join(tmp_results_dir, m), os.path.join(upload_dir, m))
            print("INFO: Upload %s to %s." % (os.path.join(tmp_results_dir, m), os.path.join(upload_dir, m)))
    shutil.rmtree(tmp_results_dir)

def query_results(list_results, machine, distro):
    qr = []
    for lr in list_results:
        if re.findall(machine, lr):
            if re.findall(distro, lr):
                qr.append(lr)
    latest_result = max(qr, key=os.path.getmtime).replace("/composite.xml", "")
    return latest_result 

def modify_config(tmp_results_dir):
    phoronix_config = "/etc/phoronix-test-suite.xml"        
    tree = ET.parse(phoronix_config)  
    root = tree.getroot()                                                                                              
    for item in root.iter('Testing'):                
        item.find('ResultsDirectory').text = tmp_results_dir  
    print("INFO: edited phoronix config to %s" % phoronix_config)
    tree.write(phoronix_config)

def publish_results(results, upload_server):
    os_name = get_os()
    suffix_path = get_boardinfo() + '/' + os_name
    upload_server = os.path.join(upload_server, suffix_path)
    if not os.path.exists(upload_server):
        os.mkdir(upload_server)
    cmd = "cp -r %s %s" % (results, upload_server)
    output = subprocess.check_output(cmd, shell=True).decode()
    print("INFO: Successfully upload to %s" % os.path.join(upload_server, get_resultsfiles(results)))

def auto_publish_results(results, upload_dir, id):
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    dest_dir = os.path.join(upload_dir, get_resultsfiles(results))
    if id is not None:
        set_identifier(results, id)
    cmd = 'cp -r %s %s' % (results, upload_dir)
    subprocess.check_output(cmd, shell=True).decode()
    print('INFO: Successfully upload to %s' % dest_dir)
    data = {"phoronixResults" : dest_dir}
    b_info = os.path.join(get_dir("lava_id_dir"), 'board_info.json')
    if os.path.isfile(b_info):
        update_board_info(get_dir("lava_id_dir"), data)
        print('INFO: Successfully updated %s' % b_info)
    else:
        print('ERROR: Unable to update %s. File is missing.' % b_info)

def set_identifier(phoronixResult, newid):
    currentResult = get_resultsfiles(phoronixResult)
    phoronixResult = os.path.join(phoronixResult, 'composite.xml')
    tree = ET.parse(phoronixResult)
    root = tree.getroot()
    for n in root.iter('System'):
        n.find('Identifier').text = newid
    for n in root.iter('Entry'):
        n.find('Identifier').text = newid
    print("INFO: Set new identifier on Phoronix result as %s" % newid)
    tree.write(phoronixResult)
    cmd = 'phoronix-test-suite refresh-graphs %s' % currentResult
    subprocess.run(cmd, shell=True)

def register_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-storage", help="path to store test results")
    parser.add_argument("--installed-tests", help="path to store installed tests")
    parser.add_argument("--compare-results", help="Compare results with others run or other platfrom.\
                         [results_dir] [machine1] [machine2] [os1] [os2] [upload_dir]", nargs = '*')
    parser.add_argument("--run-tests", help="run phoronix test suite with predefined test suites")
    parser.add_argument("--upload-results", help="upload test results to artifactorial")
    parser.add_argument("--cache-directory", help="path to store cache files")
    parser.add_argument("--proxy-address", help="Hostname of proxy server. e.g proxy.com")
    parser.add_argument("--proxy-port", help="port number of proxy server")
    parser.add_argument("--convert-json", action="store_true", help="convert phoronix test results to json format")
    parser.add_argument("--nfs-mount", help="do nfs mount by providing argument as nfsserver, src, dest", nargs = '*')
    parser.add_argument("--performance", help="set scaling_governor to performance instead of powersaver.", action="store_true")
    parser.add_argument("--id", help="set phoronix identifier such as OS name on phoronix result")
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
    perf = args.performance
    id = args.id

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
    if perf:
        print("INFO: Set scaling_governor to performance")
        cmd = "echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor"
        subprocess.run(cmd, shell=True)
    if start_tests:
        if not id:
            upload_dir = get_dir("os_release_dir")
        else:
            upload_dir = get_dir("machine_dir")
            upload_dir = os.path.join(upload_dir, id)
        run_tests(start_tests)
        if nfs_mount:
            nfs_server = args.nfs_mount[0]
            nfs_src = args.nfs_mount[1]
            nfs_dest = args.nfs_mount[2]
            do_mountnfs(nfs_server, nfs_src, nfs_dest)
        auto_publish_results(get_resultsdir(), upload_dir, id)
    if compare_results:
        results_dir = args.compare_results[0]
        machine1 = args.compare_results[1]
        machine2 = args.compare_results[2]
        os1 = args.compare_results[3]
        os2 = args.compare_results[4]
        upload_dir = args.compare_results[5]
        print("INFO: Compare phoronix results")
        auto_compare_results(results_dir, machine1, machine2, os1, os2, upload_dir)
    if upload_server:
        print("INFO: The test results will upload to server %s" % upload_server)
        publish_results(get_resultsdir(), upload_server)
    if convert_json:
        print("INFO: Convert phoronix test results to json format")
        raw_result = os.path.join(get_resultsdir(), 'composite.xml')
        if os.path.isfile(raw_result):
            convert_xmltojson(raw_result, get_dir("lava_id_dir"))
        else:
            print('ERROR: %s is not exist!' % result)
