#!/bin/bash

USER = $(id -un)
pushd /usr/src
	sudo mkdir neovim
	sudo chown $USER:$USER neovim
	git clone https://github.com/neovim/neovim
	
	pushd neovim
		make CMAKE_BUILD_TYPE=RelWithDebInfo
		sudo make install
	popd
popd
