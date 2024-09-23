#!/bin/sh

printf "Installing git, python3, curl, wget...\n"

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # ...
				printf "Linux is not yet fully supported.\n"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac OSX
		if [[ `which brew` == "" ]]; then
				printf "Installing Homebrew...\n"
				/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
		else
				printf "Using Homebrew...\n"
		fi
		to_inst=()

		if [[ `which git` == "" ]]; then
				to_inst+=("git")
		fi
		if [[ `which python3` == "" ]]; then
				to_inst+=("python3")
		fi
		if [[ `which curl` == "" ]]; then
				to_inst+=("curl")
		fi
		if [[ `which wget` == "" ]]; then
				to_inst+=("wget")
		fi

		if [[ "$to_inst" ]]; then
				brew install $to_inst
		fi
elif [[ "$OSTYPE" == "cygwin" ]]; then
    # POSIX compatibility layer and Linux environment emulation for Windows
		printf "Cygwin is not yet fully supported.\n"
elif [[ "$OSTYPE" == "msys" ]]; then
    # Lightweight shell and GNU utilities compiled for Windows (part of MinGW)
		printf "Msys is not yet fully supported.\n"
elif [[ "$OSTYPE" == "win32" ]]; then
    # I'm not sure this can happen.
		printf "Win32 is not yet fully supported.\n"
elif [[ "$OSTYPE" == "freebsd"* ]]; then
		printf "FreeBSD is not yet fully supported.\n"
		to_inst=()

		if [[ `which git` == "" ]]; then
				to_inst+=("git")
		fi
		if [[ `which python3` == "" ]]; then
				to_inst+=("python3")
		fi
		if [[ `which curl` == "" ]]; then
				to_inst+=("curl")
		fi
		if [[ `which wget` == "" ]]; then
				to_inst+=("wget")
		fi

		if [[ "$to_inst" ]]; then
				su root -c "pkg install $to_inst"
		fi
else
    # Unknown.
		printf "This OS ($OSTYPE) is not yet fully supported.\n"
fi

git clone https://github.com/eturnq/unix-dotfiles ~/.config/unix-dotfiles
python3 ~/.config/unix-dotfiles/install_stage2.py
