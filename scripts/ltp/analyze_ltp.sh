#!/bin/bash

OUTPUT_FILE="analyze_ltp_results.csv"
LAVA_DIR=`ls / | grep lava`
lava_id=${LAVA_DIR/lava-/}
UPLOAD_DIR="/srv/data/LAVA/lava-job"
LTP_RESULTS_DIR="$UPLOAD_DIR/$lava_id/ltp_results"
testcases=`ls $LTP_RESULTS_DIR`

echo "Analyze LTP results"
echo -e "---------------------\n"
echo "test name, pass, fail, skip, total"
echo "----------------------------------"
for t in $testcases; do
    t="$LTP_RESULTS_DIR/$t"
    #echo "[  INFO  ] Analyzing $t"
    pass=`cat $t | grep PASS | wc -l`
    fail=`cat $t | grep FAIL | wc -l`
    skip=`cat $t | grep CONF | wc -l`
    total=$(( pass + fail + skip ))
    test_name=${t%%-*[a-zA-Z]}
    test_name=${test_name/ltp_results\//}
    echo "$test_name, $pass, $fail, $skip, $total"   2>&1 | tee -a $UPLOAD_DIR/$lava_id/$OUTPUT_FILE
done

