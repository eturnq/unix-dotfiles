#!/bin/sh

mkdir -p $HOME/.zsh
git clone https://github.com/sindresorhus/pure $HOME/.zsh/pure
echo "Changing shell to $(which zsh) for user $(id -un)"
sudo chsh -s $(which zsh) $(id -un)
