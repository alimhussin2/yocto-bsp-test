#!/bin/bash

RESULT="sanity_test.log"
UPLOAD_DIR="/srv/data/LAVA/lava-job"

echo "[  INFO  ] Sanity test started"
# check kernel version
uname -a >> $RESULT

# check dmesg
dmesg | grep -i -e 'error|fail' >> $RESULT

# upload result
lava_job=`ls / | grep lava`
lava_id=${lava_job/lava-/}
UPLOAD_DIR=$UPLOAD_DIR/$lava_id
cp $RESULT $UPLOAD_DIR
echo "[  INFO  ] Sanity test completed"

