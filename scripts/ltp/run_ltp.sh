#!/bin/bash

# Description: Linux Test Project (LTP) 

LTP_REPO="ltp.tar.xz"
NFS_DIR="/srv/data/LAVA/kernel"
UPLOAD_DIR="/srv/data/LAVA/lava-job"
LAVA_DIR=`ls / | grep lava`
lava_id=${LAVA_DIR/lava-/}
LAVA_PROXY="/$LAVA_DIR/bin/lava-proxy"
SKIPFILES="skipfiles/skipfile-mturbot"

source $LAVA_PROXY
cd $HOME
echo "[  INFO  ] Clone from linux test project repo"
git clone https://github.com/linux-test-project/ltp.git

if [[ ! $? -eq 0 ]]; then
    echo "[  ERROR  ] Unable to clone from remote repo."
    echo "[  INFO  ] Copy from NFS: $NFS_DIR"
    cp $NFS_DIR/$LTP_REPO $HOME
    echo "[  INFO  ] Extracting $LTP_REPO"
    tar -xJf $HOME/$LTP_REPO
fi

UPLOAD_DIR="$UPLOAD_DIR/$lava_id/ltp_results"

if [[ ! -d "$UPLOAD_DIR" ]]; then
    mkdir -p $UPLOAD_DIR
fi

cd $HOME/ltp
echo "[  INFO  ] Make autotools"
make autotools 2>&1 | tee make_autotools.log
cp make_autotools.log $UPLOAD_DIR

echo "[  INFO  ] Configure LTP"
./configure 2>&1 | tee ltp_configure.log
cp ltp_configure.log $UPLOAD_DIR

echo "[  INFO  ] Make LTP"
make 2>&1 | tee make_ltp.log
cp make_ltp.log $UPLOAD_DIR

echo "[  INFO  ] Install LTP"
make install 2>&1 | tee install_ltp.log
cp install_ltp.log $UPLOAD_DIR

export PATH="$PATH:/otp/ltp"
ltp_path=`which runltp`
echo "[  INFO  ] Run LTP"

testcases=`ls /opt/ltp/runtest`
for t in ${testcases[@]}; do
    echo "[  INFO  ] Testing $t"
    if [[ ! -z $ltp_path ]]; then
        runltp -p -f $t -S $SKIPFILES -l $UPLOAD_DIR/$t-`date +"%Y_%m_%d-%H_%M_%S"`.log
    else
       /opt/ltp/runltp -p -f $t -S $SKIPFILES -l $UPLOAD_DIR/$t-`date +"%Y_%m_%d-%H_%M_%S"`.log
   fi
done
