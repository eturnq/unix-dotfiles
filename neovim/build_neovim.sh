#!/usr/bin/env bash

USER=$(id -un)
su - $USER -c "nvm install --lts" # NPM is required for some Neovim packages.

pushd /usr/src
	sudo mkdir neovim
	sudo chown $USER:$USER neovim
	git clone https://github.com/neovim/neovim
	
	pushd neovim
		make CMAKE_BUILD_TYPE=RelWithDebInfo
		sudo make install
	popd
popd
