#!/bin/bash

# Description: Download kselftest, run & parse the result. 
# The output result is results-summary-kselftest-version.log

LINUX_MIRROR="http://mirrors.edge.kernel.org/pub/linux/kernel/v4.x/"
DEFAULT_KSELFTEST="/srv/data/LAVA/kernel/kselftest-4.14.tar.gz"
LOGFILE="kselftest-`uname -r`.log"
RESULT_FILE="results-$LOGFILE"
LOGFILE_TEMP="$LOGFILE.temp"
RESULT_TEMP="$RESULT_FILE.temp"
RESULT_SUMMARY="results-summary-$LOGFILE"
RESULT_COMPONENTS="results-by-component-$LOGFILE"

usage() {
    echo "Usage :$0 [-u|--url,                  url of kselftest]
                    [-U|--upload,               path to uploaded file]
                    [-a|--analyze [filename],   analyze kselftest result]"
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

list_components_result() {
    cat $RESULT_FILE | grep -E '(PASS|FAIL|SKIP)' | awk -F '_' '{ print $1 }' | grep -v "test" > $RESULT_TEMP
    echo "Summary by components"
    echo "============================="
    echo "  Components, Pass, Fail, Skip"
    local n=0
    while true;
    do
        local components=$(head -n1 $RESULT_TEMP)
        if [[ -z $components ]]; then
            break
        else
            cpass=`cat $RESULT_FILE | grep PASS | grep $components | wc -l`
            cfail=`cat $RESULT_FILE | grep FAIL | grep $components | wc -l`
            cskip=`cat $RESULT_FILE | grep SKIP | grep $components | wc -l`
            sed -i "/$components/d" $RESULT_TEMP
            #echo "   $components:  (PASS=$cpass | FAIL=$cfail | SKIP=$cskip)"
            echo "  $components, $cpass, $cfail, $cskip"
            n=$(( n+1 ))
        fi
    done
    echo -e "\n============================"
    echo -e "Total components tested: $n\n\n"
}

details_by_components() {
    cat $RESULT_FILE | grep -E '(PASS|FAIL|SKIP)' | awk -F '_' '{ print $1 }' | grep -v "test" > $RESULT_TEMP
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
    list_components_result
    details_by_components
}

cleanup() {
    rm $LOGFILE_TEMP $RESULT_TEMP $RESULT_FILE
}

option() {
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -u|--url)
                if [[ ! -z "$2" ]]; then
                    if [[ "$2" == "default" ]]; then
                        echo "Download kselftest from kernel mirror"
                        version=`uname -r`
                        kernel_version=${version//[a-zA-Z-]/}
                        echo "Downloading ${LINUX_MIRROR}/linux-${kernel_version}.tar.xz"
                        wget ${LINUX_MIRROR}/linux-${kernel_version}.tar.xz
                    elif [[ -z "${2##*http*}" ]]; then
                        echo "Download kselftest from given url"
                        wget $2 -O linux-$kernel_version.tar.xz
                    else
                        echo "Input error. See usage"
                        usage
                    fi
                    if [ -f "linux-${kernel_version}.tar.xz" ]; then
                        tar -xJf "linux-${kernel_version}.tar.xz"
                    else
                        echo "[  Error  ] linux-${kernel_version}.tar.xz not found!"
                        exit 1
                    fi
                    if [[ -f "$RESULT_COMPONENTS" ]]; then
                        rm -f "$RESULT_SUMMARY" "$RESULT_COMPONENTS"
                    fi
                    make -C $PWD/linux-$kernel_version/tools/testing/selftests run_tests 2>&1 | tee ${LOGFILE}
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
                cleanup
                exit 0
            ;;
            -a|--analyze)
                echo "Analyze kselftest results"
                if [[ -z "$2" ]]; then
                    echo "Kselftest results file missing. Abort"
                    usage
                else
                    LOGFILE=$2
                    OUTPUT_ANALYZE=results-by-component-$LOGFILE
                    analyze_kselftest_results >> $OUTPUT_ANALYZE
                    echo "Complete analyzing kselftest results"
                fi
                cleanup
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
cleanup
