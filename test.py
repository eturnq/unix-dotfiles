#!/usr/bin/env python3

#from py_mod.install_dep import install_archive
from py_mod.install_dep import get_package_manager

def main():
    #install_archive("~/Downloads/Noto.zip", "bar")
    print(get_package_manager())

if __name__ == "__main__":
    main()
