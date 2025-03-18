#!/bin/bash

USER=$(id -un)
PKG=$(python3 -c "from py_mod.install_dep import get_package_manager ; print(get_package_manager())")
if [ $PKG -eq "apt-get" ] ; then
	INITSVC=""
elif [ $PKG -eq "xbps-install" ] ; then
	INITSVC="-DINIT_SYSTEM=runit"
else
	INITSVC=""
fi

sudo mkdir -p /usr/src/ly
sudo chown $USER:$USER /usr/src/ly
git clone https://codeberg.org/AnErrupTion/ly /usr/src/ly

pushd /usr/src/ly
	git pull
	$HOME/.local/bin/zig build $INISVC
	sudo $HOME/.local/bin/zig build installexe
popd
