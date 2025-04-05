#!/usr/bin/env bash

NEOVIM_VERSION=v0.11.0

USER=$(id -un)
[[ `uname` != "FreeBSD" ]] && su - $USER -c "nvm install --lts" # NPM is required for some Neovim packages.

[[ $(type -p "gmake") ]] && MAKE="gmake" || MAKE="make" # Use gmake if it is installed, otherwise make

pushd /usr/src
	sudo mkdir neovim
	sudo chown $USER:$USER neovim
	git clone https://github.com/neovim/neovim
	
	pushd neovim
		git checkout $NEOVIM_VERSION
		$MAKE CMAKE_BUILD_TYPE=RelWithDebInfo
		sudo $MAKE install
	popd
popd
