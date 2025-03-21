#!/usr/bin/env bash

USER=$(id -un)
su - $USER -c "nvm install --lts" # NPM is required for some Neovim packages.

pushd /usr/src
	sudo mkdir neovim
	sudo chown $USER:$USER neovim
	git clone https://github.com/neovim/neovim
	
	pushd neovim
		gmake CMAKE_BUILD_TYPE=RelWithDebInfo
		sudo gmake install
	popd
popd
