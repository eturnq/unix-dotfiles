#!/usr/bin/env python3

import argparse
import sys

from py_mod.install_module import get_modules

def main():
    args = parseargs()
    print(args)

    if args.command == "install":
        install_modules(args.modules)
    else:
        print("Invalid command.")

def parseargs():
    parser = argparse.ArgumentParser(prog="install_module", description="Install modules from this repo.")
    parser.add_argument("command", action="store")
    parser.add_argument("modules", action="store", nargs="+")
    return parser.parse_args(sys.argv[1:])

def install_modules(modules):
    for mod in filter(lambda m: m.name() in modules, get_modules()):
        if mod.do_install():
            print("{} is installed.".format(mod.name()))
        else:
            print("Error installing {}.".format(mod.name()))

if __name__ == "__main__":
    main()
