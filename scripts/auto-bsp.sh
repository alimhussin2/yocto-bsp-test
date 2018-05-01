#!/bin/bash -xe

cat ~/.gitconfig
socat -V
git --version

cd $HOME
pwd
#git clone git://git.yoctoproject.org/poky
git clone http://git.yoctoproject.org/git/poky
cd $HOME/poky
git checkout $GIT_COMMIT_ID
source oe-init-build-env

echo "INHERIT += \"testimage\"
TEST_TARGET = \"simpleremote\"
TEST_SERVER_IP = \"$SERVER_IP\"
TEST_TARGET_IP = \"$DUT_IP\"
MACHINE = \"$TARGET_MACHINE\"" >> $HOME/poky/build/conf/local.conf

bitbake rpm busybox curl run-postinsts
bitbake package-index

ls $HOME/poky/build/tmp/deploy/images/$TARGET_MACHINE
bitbake $IMAGE_TESTED -c testimage

echo "Test $IMAGE_TESTED completed"
