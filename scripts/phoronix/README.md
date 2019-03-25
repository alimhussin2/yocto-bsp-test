phoronix test suite parser script
================================

phoronix.py is a parse script used to run phoronix using batch-benchmark.
The testsuites located in testsuites directory covered processor and memory
tests.

How to use phoronix.py?
======================
Configure phoronix test suite
$ ./phoronix.py --proxy-port <proxyPort> --proxy-address <proxyAddress>--results-storage /phoronix-test-suite/test-results/machines --installed-tests /phoronix-test-suite/installed-tests --cache-directory /phoronix-test-suite/download-cache

Run phoronix
$ ./phoronix.py --run-tests testsuites/processor_suites.txt

upload results to NFS server
$ mount nfsserver:/path/to/nfs /path/to/share
$ ./phoronix.py --upload-results /path/to/share/

NOTE: the --upload-results option would create a file structure as follow
/path/to/share/<board_name>/<os-release>
