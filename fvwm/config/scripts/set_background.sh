#!/usr/bin/env bash

[[ $(type -P "fvwm3-root") ]] && fvwm3-root $1 || fvwm-root $1
