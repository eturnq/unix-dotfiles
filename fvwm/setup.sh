#!/bin/bash

sudo update-alternatives --install /usr/bin/x-terminal-emulator x-terminal-emulator $(which xterm) 20

pushd /tmp
	wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/Noto.zip
popd

mkdir -p $(HOME)/.fonts
pushd $(HOME)/.fonts
	unzip /tmp/Noto.zip
popd

rm /tmp/Noto.zip

fc-cache
xrdb $(HOME)/.Xresources
