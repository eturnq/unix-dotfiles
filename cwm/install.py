#!/usr/bin/env python3

import subprocess
from os.path import exists
from os.path import join as join_path
from os.path import realpath
from os.path import expanduser as user_path
from pathlib import Path as FsItem
from shutil  import copyfile

def main():
    print("Install script for CWM config.")

    print("Checking dependencies...")
    if not check_dependencies(): return -1
    print("All dependencies found.")

    print("\nInstall .config/cwm symlink")
    cwm_tgt = user_path("~/.config/cwm")
    if not install_link(realpath(""), cwm_tgt): return -1

    print("\nInstall .xinitrc")
    xrc_src = realpath(".xinitrc")
    xrc_tgt = user_path("~/.xinitrc")
    if not install_file(xrc_src, xrc_tgt): return -1

    print("\nInstall .Xresources and .Xdefaults")
    xresources_src = realpath(".Xresources")
    xresources_tgt = user_path("~/.Xresources")
    xdefaults_tgt  = user_path("~/.Xdefaults")
    if not install_file(xresources_src, xresources_tgt): return -1
    if not install_link(xresources_tgt, xdefaults_tgt): return -1

    print("\nInstall default wallpaper")
    wp_dir = user_path("~/Pictures/Wallpaper")
    default_wp_src = realpath("default.jpg")
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
            procOut = subprocess.run(["which", dep], capture_output=True)
            if procOut.returncode != 0:
                print("\t{} not found. Please install".format(dep))
                return False
            print("\t{} found".format(dep))
    return True

def item_exists(fs_item):
    try:
        stat = fs_item.lstat()
        return True
    except Exception as e:
        return False

def install_file(source, target, is_link=False):
    src = FsItem(source)
    tgt = FsItem(target)

    if not src.exists():
        print("\tError: {} doesn't exist in repo!".format(source))
        return False

    if item_exists(tgt):
        print("Target {} exists".format(target))
        user_input = input("Overwrite? (yes/no[default]): ")
        user_input = user_input.lower()
        is_affirm = user_input == "yes" or user_input == "y"
        if not is_affirm: return True # Don't overwrite, just continue
        tgt.unlink()

    try:
        if is_link:
            tgt.symlink_to(src)
            print("linked {} to {}".format(source, target))
        else:
            copyfile(src, tgt)
            while not item_exists(tgt): pass
            print("copied {} to {}".format(source, target))
    except Exception as e:
        print("\tError: {}".format(e))
        return False

    return True

def install_link(source, target):
    return install_file(source, target, True)
    
if __name__ == "__main__":
    main()
