#!/bin/bash -x

RESULT="sanity_test.log"
UPLOAD_DIR="/srv/data/LAVA/lava-job"

echo "[  INFO  ] Sanity test started"
echo "check kernel version" 2>&1 | tee $RESULT
uname -a 2>&1 | tee -a $RESULT

echo "check dmesg" 2>&1 | tee -a $RESULT
echo "------------------" 2>&1 | tee -a $RESULT
dmesg | grep -i -E 'error|fail' 2>&1 | tee -a $RESULT

# upload result
lava_job=`ls / | grep lava`
lava_id=${lava_job/lava-/}
UPLOAD_DIR=$UPLOAD_DIR/$lava_id
if [[ ! -d $UPLOAD_DIR ]]; then
    mkdir $UPLOAD_DIR
fi
cp $RESULT $UPLOAD_DIR
if [[ $? -eq 0 ]]; then
    echo "[  INFO  ] Upload result to $UPLOAD_DIR/$RESULT"
else
    echo "[  ERROR  ] Unable to upload result to $UPLOAD_DIR/$RESULT"
fi
echo "[  INFO  ] Sanity test completed"

