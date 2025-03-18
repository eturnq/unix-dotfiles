#!/bin/bash

USER=$(id -un)
SRCDIR=/usr/src/ly

PKG=$(python3 -c "from py_mod.install_dep import get_package_manager ; print(get_package_manager())")
if [ $PKG = "apt-get" ] ; then
	INITSVC=""
elif [ $PKG = "xbps-install" ] ; then
	INITSVC="-DINIT_SYSTEM=runit"
else
	INITSVC=""
fi

sudo mkdir -p $SRCDIR
sudo chown $USER:$USER $SRCDIR
git clone https://codeberg.org/AnErrupTion/ly $SRCDIR

pushd $SRCDIR
	git pull
	$HOME/.local/bin/zig build $INITSVC
	sudo $HOME/.local/bin/zig build installexe
popd
