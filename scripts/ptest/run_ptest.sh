#!/bin/bash

RESULTS_DIR="/home/root/ptest-results"
NFS_DIR="/srv/data/LAVA/lava-job"

which ptest-runner
if [[ ! $? -eq 0 ]]; then
    echo "[  ERROR  ] Ptest-runner is not install"
    exit 1
fi

job=`ls / | grep lava`
JOB_ID=${job/lava-/}
if [ ! -d $RESULTS_DIR ]; then
    echo "[  INFO  ] Creating $RESULTS_DIR"
    mkdir $RESULTS_DIR
fi

NFS_DIR=$NFS_DIR/$JOB_ID
if [ ! -d "$NFS_DIR/ptest-results" ]; then
    echo "[  INFO  ] Creating $NFS_DIR/ptest-results"
    mkdir $NFS_DIR/ptest-results
fi

echo "[  INFO  ] ptest-runner started"
ptest_list=`ptest-runner -l | awk -F ' ' '{ print $1 }'`
for pt in $ptest_list;
do
    echo "ptest: $pt"
    lava-test-case "ptest-runner-$pt" --shell "ptest-runner $pt 2>&1 | tee $RESULTS_DIR/$pt.log"
    cp $RESULTS_DIR/$pt.log $NFS_DIR
done

echo "[  INFO  ] ptest-runner completed"


