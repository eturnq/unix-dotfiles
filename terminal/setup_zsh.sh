#!/bin/sh

UNAME=`uname`
SUDO=sudo
if [ $UNAME = "OpenBSD" ]; then
    SUDO=doas
fi

mkdir -p $HOME/.zsh
git clone https://github.com/sindresorhus/pure $HOME/.zsh/pure
echo "Changing shell to $(which zsh) for user $(id -un)"
$SUDO chsh -s $(which zsh) $(id -un)
