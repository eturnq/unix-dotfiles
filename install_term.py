#!/usr/bin/env python3

import importlib.util
import sys
install_dep_spec = importlib.util.spec_from_file_location("py_lib.install_dep", "py_mod/install_dep.py")
install_dep = importlib.util.module_from_spec(install_dep_spec)
sys.modules["py_lib.install_dep"] = install_dep
install_dep_spec.loader.exec_module(install_dep)

from py_lib.install_dep import exe_in_path
from py_lib.install_dep import install_file
from py_lib.install_dep import install_link

from py_lib.install_dep import join_path
from py_lib.install_dep import real_path
from py_lib.install_dep import user_path


def main():
    print("Install script for tmux and nvim configuration.")

    print("Install .tmux.conf")
    if not install_file(real_path(".tmux.conf"), user_path("~/.tmux.conf")): return -1
    print("Install nvim config")
    if not install_link(real_path("nvim"), user_path("~/.config/nvim")): return -1

if __name__ == "__main__":
    main()
