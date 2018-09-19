#!/bin/bash

# Description: Download kselftest, run & parse the result. 
# The output result is results-summary-kselftest-version.log

DEFAULT_KSELFTEST="/srv/data/LAVA/kernel/kselftest-4.14.tar.gz"
LOGFILE="kselftest-`uname -r`.log"
RESULT_FILE="results-$LOGFILE"
LOGFILE_TEMP="$LOGFILE.temp"
RESULT_TEMP="$RESULT_FILE.temp"
RESULT_SUMMARY="results-summary-$LOGFILE"
RESULT_COMPONENTS="results-by-component-$LOGFILE"

usage() {
    echo "Usage :$0 [-u|--url,    url of kselftest]
                    [-U|--upload, path to uploaded file]"
    exit 1
}
parse_output() {
    sed -r 's/(.*selftests: (\S+): (\S+) \[(.*)\])/\1\nselftests: \2_\3 [\4]/' "${LOGFILE}" > "${LOGFILE_TEMP}"
    grep "selftests:" "${LOGFILE_TEMP}" > "${RESULT_FILE}"
    sed -i -e 's/: /-/g' "${RESULT_FILE}"
    sed -i -e 's/\[//g' "${RESULT_FILE}"
    sed -i -e 's/]//g' "${RESULT_FILE}"
    sed -i -e 's/selftests-//g' "${RESULT_FILE}"
    sed -i '/ok/d' "${RESULT_FILE}"
    sed -i '/not ok/d' "${RESULT_FILE}"
}

summary() {
    test_pass=`grep "PASS" "${RESULT_FILE}" | wc -l`
    test_fail=`grep "FAIL" "${RESULT_FILE}" | wc -l`
    test_skip=`grep "SKIP" "${RESULT_FILE}" | wc -l`
    echo "Summary kselftest"
    echo "================="
    echo "Total test cases: $(( test_pass + test_fail + test_skip ))"
    echo "PASS: $test_pass"
    echo "FAIL: $test_fail"
    echo -e "SKIP: $test_skip\n"

}

details() {
    echo -e "\nSummary details"
    echo "=============================="
    echo -e "\nTest Pass"
    echo "=============================="
    grep "PASS" ${RESULT_FILE}
    echo -e "\nTest Fail"
    echo "=============================="
    grep "FAIL" ${RESULT_FILE}
    echo -e "\nTest Skip"
    echo "=============================="
    grep "SKIP" ${RESULT_FILE}
}

details_by_components() {
    cat $RESULT_FILE | grep PASS | awk -F '_' '{ print $1 }' > $RESULT_TEMP
    while true;
    do
        component=$(head -n1 $RESULT_TEMP)
        if [[ -z $component ]]; then
            break
        else
            echo "component: $component"
            echo "====================="
            c_pass=`cat $RESULT_FILE | grep PASS | grep $component | wc -l`
            c_fail=`cat $RESULT_FILE | grep FAIL | grep $component | wc -l`
            c_skip=`cat $RESULT_FILE | grep SKIP | grep $component | wc -l`
            echo "PASS: $c_pass"
            echo "FAIL: $c_fail"
            echo "SKIP: $c_skip"
            echo -e "Total: $(( c_pass + c_fail + c_skip ))\n"
            cat $RESULT_FILE | grep PASS | grep $component
            cat $RESULT_FILE | grep FAIL | grep $component
            cat $RESULT_FILE | grep SKIP | grep $component
            sed -i "/$component/d" $RESULT_TEMP 
            echo -e '\n'
        fi
    done
}

info() {
    kernel_version=`uname -r`
    arch=`uname -m`
    lava_job=`ls / | grep lava`; lava_id=${lava_job/lava-/}
    platform="minnowboard"
    hostname=`hostname`
    echo "BOARD INFORMATION"
    echo "==================="
    echo "KERNEL VERSION: $kernel_version"
    echo "ARCH          : $arch"
    echo "PLATFORM      : $platform"
    echo "HOSTNAME      : $hostname"
    echo "LAVA JOB ID   : $lava_id"
    echo -e "===================\n"
}

analyze_kselftest_results() {
    parse_output
    info
    summary
    details_by_components
}

option() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -u|--url)
                if [[ ! -z "$2" ]]; then
                    if [[ "$2" == "default" ]]; then
                        echo "Download kselftest from local directory"
                        cp $DEFAULT_KSELFTEST .
                    elif [[ -z "${2##*http*}" ]]; then
                        echo "Download kselftest from given url"
                        wget $2 -O kselftest-4.14.tar.gz
                    else
                        echo "Input error. See usage"
                        usage
                    fi
                    tar xf "kselftest-4.14.tar.gz"
                    cd "kselftest"
                    if [[ -f "$RESULT_COMPONENTS" ]]; then
                        rm -f "$RESULT_SUMMARY" "$RESULT_COMPONENTS"
                    fi
                    ./run_kselftest.sh 2>&1 | tee ${LOGFILE}
                    analyze_kselftest_results >> $RESULT_COMPONENTS
                else
                    echo "Unable to execute kselftest. No url given"
                    exit 1
                fi
            ;;
            -U|--upload)
                UPLOADED_DIR=$2
                lava_job=`ls / | grep lava`; lava_id=${lava_job/lava-/}
                UPLOADED_DIR="$UPLOADED_DIR/$lava_id"
                if [[ ! -d $UPLOADED_DIR ]]; then
                    mkdir $UPLOADED_DIR
                fi
                echo "Upload result to $UPLOADED_DIR"
                cp $RESULT_COMPONENTS $UPLOADED_DIR
                cp $LOGFILE $UPLOADED_DIR
                exit 0
            ;;
            *)
                usage
            ;; 
        esac
        shift
        shift
    done
}

main() {
    if [ "$#" -eq 0 ]; then
        usage
    else
        option "${POSITIONAL[@]}"
    fi
}

POSITIONAL=()
POSITIONAL+=("$@")
main "${POSITIONAL[@]}"

