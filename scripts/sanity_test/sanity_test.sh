#!/bin/bash -x

RESULT="sanity_test.log"
UPLOAD_DIR="/srv/data/LAVA/lava-job"

echo "[  INFO  ] Sanity test started"
echo "check kernel version" >> $RESULT
uname -a >> $RESULT

echo "check dmesg" >> $RESULT
dmesg | grep -i -e 'error|fail' >> $RESULT

# upload result
lava_job=`ls / | grep lava`
lava_id=${lava_job/lava-/}
UPLOAD_DIR=$UPLOAD_DIR/$lava_id
cp $RESULT $UPLOAD_DIR
echo "[  INFO  ] Upload result to $UPLOAD_DIR/$RESULT"
echo "[  INFO  ] Sanity test completed"

