#!/bin/bash -xe

# metadata for YP poky release
# git://git.yoctoproject.org/poky

GIT_COMMIT_ID="9e3a9637b8f86f504e187b96cd0c98d8e1f651da"
SERVER_IP="localhost"
DUT_IP="localhost"
TARGET_MACHINE="intel-corei7-64"
IMAGE_TESTED="core-image-sato"

# create a file for git_proxy
echo '#!/bin/bash -xe
exec socat STDIO SOCKS4:localhost:$1:$2,socksport=1080' > /usr/bin/git_proxy_command
chmod 755 /usr/bin/git_proxy_command
ls -lah /usr/bin/git_proxy_command
cat /usr/bin/git_proxy_command

# configure proxy
export http_proxy="http://localhost:80"
export https_proxy="http://localhost:80"
export ftp_proxy="http://localhost:80"
export socks_proxy="http://localhost:80"
export GIT_PROXY_COMMAND=/usr/bin/git_proxy_command
export LC_ALL="en_US.UTF-8"

# configure git
git config --global user.name "minnow"
git config --global user.email minnow@test
git config --global http.proxy $http_proxy
git config --global https.proxy $https_proxy
git config --global socks.proxy $socks_proxy
