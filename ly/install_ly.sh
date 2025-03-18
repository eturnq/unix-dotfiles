#!/bin/bash

USER=$(id -un)

sudo mkdir -p /usr/src/ly
sudo chown $USER:$USER /usr/src/ly
git clone https://codeberg.org/AnErrupTion/ly /usr/src/ly

pushd /usr/src/ly
	$HOME/.local/bin/zig build
	sudo $HOME/.local/bin/zig build installexe
popd
