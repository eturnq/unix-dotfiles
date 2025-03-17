#!/bin/bash
pushd /tmp
	wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.3.0/Noto.zip
popd

mkdir -p $(HOME)/.fonts
pushd $(HOME)/.fonts
	unzip /tmp/Noto.zip
popd

rm /tmp/Noto.zip
