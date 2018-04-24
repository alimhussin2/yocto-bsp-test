#!/bin/bash -xe

COMMIT_ID="9e3a9637b8f86f504e187b96cd0c98d8e1f651da"
SERVER_IP="192.168.122.2"
DUT_IP="192.168.122.100"
TARGET_MACHINE="intel-corei7-64"
IMAGE_TESTED="core-image-sato"

export http_proxy="http://192.168.122.2:9111"
export https_proxy="http://192.168.122.2:9111"
export ftp_proxy="http://192.168.122.2:9111"
export socks_proxy="http://192.168.122.2:1080"
export LC_ALL="en_US.UTF-8"

echo '#!/bin/bash -xe
exec socat STDIO SOCKS4:192.168.122.2:$1:$2,socksport=1080' > /usr/bin/git_proxy_command
chmod 755 /usr/bin/git_proxy_command
ls -lah /usr/bin/git_proxy_command
cat /usr/bin/git_proxy_command
export GIT_PROXY_COMMAND=/usr/bin/git_proxy_command

git config --global user.name "minnow"
git config --global user.email minnow@test
git config --global http.proxy $http_proxy
git config --global https.proxy $https_proxy
git config --global socks.proxy $socks_proxy
cat ~/.gitconfig

socat -V
git --version

cd $HOME
pwd
#git clone git://git.yoctoproject.org/poky
git clone http://git.yoctoproject.org/git/poky
cd $HOME/poky
git checkout $COMMIT_ID
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
