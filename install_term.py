#!/usr/bin/env python3

import importlib.util
import sys
install_dep_spec = importlib.util.spec_from_file_location("py_lib.install_dep", "py_mod/install_dep.py")

if install_dep_spec is not None:
    install_dep = importlib.util.module_from_spec(install_dep_spec)
    sys.modules["py_lib.install_dep"] = install_dep
    if install_dep_spec.loader is not None:
        install_dep_spec.loader.exec_module(install_dep)

install_mod_spec = importlib.util.spec_from_file_location("py_lib.install_mod", "py_mod/install_module.py")
if install_mod_spec is not None:
    install_mod = importlib.util.module_from_spec(install_mod_spec)
    sys.modules["py_lib.install_mod"] = install_mod
    if install_mod_spec.loader is not None:
        install_mod_spec.loader.exec_module(install_mod)

#from py_lib.install_dep import exe_in_path # type: ignore
#from py_lib.install_dep import install_file # type: ignore
from py_lib.install_dep import install_link # type: ignore
from py_lib.install_dep import install_package # type: ignore

from py_lib.install_mod import get_modules # type: ignore


def main():
    print("Install script for tmux and nvim configuration.")

    for m in get_modules():
        if m.do_install():
            print("{} is installed.".format(m.name()))
        else:
            print("Error installing {}.".format(m.name()))

    #print("Install .tmux.conf")
    #if not install_link("terminal/.tmux.conf", "~/.tmux.conf"): return -1
    print("Install nvim config")
    if not install_link("nvim", "~/.config/nvim"): return -1
    install_package(["git","zsh"])

if __name__ == "__main__":
    main()
