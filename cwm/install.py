#!/usr/bin/env python3

import importlib.util
import sys
install_dep_spec = importlib.util.spec_from_file_location("py_lib.install_dep", "../py_mod/install_dep.py")
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
    print("Install script for CWM config.")

    print("Checking dependencies...")
    if not check_dependencies(): return -1
    print("All dependencies found.")

    print("\nInstall .config/cwm symlink")
    cwm_tgt = user_path("~/.config/cwm")
    if not install_link(real_path(""), cwm_tgt): return -1

    print("\nInstall .xinitrc")
    xrc_src = real_path(".xinitrc")
    xrc_tgt = user_path("~/.xinitrc")
    if not install_file(xrc_src, xrc_tgt): return -1

    print("\nInstall .Xresources and .Xdefaults")
    xresources_src = real_path(".Xresources")
    xresources_tgt = user_path("~/.Xresources")
    xdefaults_tgt  = user_path("~/.Xdefaults")
    if not install_file(xresources_src, xresources_tgt): return -1
    if not install_link(xresources_tgt, xdefaults_tgt): return -1

    print("\nInstall default wallpaper")
    wp_dir = user_path("~/Pictures/Wallpaper")
    default_wp_src = real_path("default.jpg")
    default_wp_tgt = join_path(wp_dir, "default.jpg")
    current_wp_tgt = join_path(wp_dir, "current.wallpaper")
    if not install_file(default_wp_src, default_wp_tgt): return -1
    if not install_link(default_wp_tgt, current_wp_tgt): return -1

    print("\n\nSuccess!")
    print("CWM config installed. Run `startx` to use.")

def check_dependencies():
    with open("./dep.txt", "r") as deps:
        for line in deps.readlines():
            dep = line.rstrip()
            if not exe_in_path(dep).success:
                print("\t{} not found. Please install".format(dep))
                return False
            print("\t{} found".format(dep))
    return True
   
if __name__ == "__main__":
    main()
