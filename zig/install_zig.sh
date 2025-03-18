#!/bin/bash

ZIG_URL=https://ziglang.org/download
ZIG_VERSION=0.14.0
ZIG_FILENAME=zig-linux-x86_64-$ZIG_VERSION
ZIG_ARCHIVE=$ZIG_FILENAME.tar.xz

mkdir -p $HOME/.local/{bin,share}
pushd $HOME/.local/share
	wget $ZIG_URL/$ZIG_VERSION/$ZIG_ARCHIVE
	tar xf $ZIG_ARCHIVE
	mv $ZIG_FILENAME zig
popd

pushd $HOME/.local/bin
	ln -s ../share/zig/zig zig
popd
