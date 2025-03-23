#!/usr/bin/env bash

CMD1="fvwm3-menu-desktop"
CMD2="fvwm-menu-desktop"
[[ $(type -P "$CMD1") ]] && $CMD1 $@ || $CMD2 $@
