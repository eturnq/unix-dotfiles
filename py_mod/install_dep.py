import subprocess

from os.path import join as join_path
from os.path import realpath as real_path
from os.path import expanduser as user_path
from pathlib import Path as FsItem
from shutil  import copyfile

class DepResponse:
    def __init__(self, success, message=""):
        self.success = success
        self.message = message

def exe_in_path(exe):
    success = True
    message = "{} found".format(exe)

    procOut = subprocess.run(["which", exe], capture_output=True)
    if procOut.returncode != 0:
        message = "{} not found. Please install".format(exe)
        success = False

    return DepResponse(success, message)

def fs_item_exists(fs_item):
    try:
        stat = fs_item.lstat()
        return True
    except Exception as e:
        return False

def install_file(source, target, is_link=False):
    success = True
    message = "{} {} to {}".format("{}", source, target)

    src = FsItem(source)
    tgt = FsItem(target)

    if not src.exists():
        return DepResponse(False, "{} doesn't exist".format(source))

    if fs_item_exists(tgt):
        print("Target {} exists".format(target))
        user_input = input("Overwrite? (yes/no[default]): ").lower()
        is_affirm = user_input == "yes" or user_input == "y"
        if not is_affirm: return DepResponse(True, "Not overwriting target")
        tgt.unlink()

    try:
        if is_link:
            tgt.symlink_to(src)
            message = message.format("linked")
        else:
            copyfile(src, tgt)
            while not fs_item_exists(tgt): pass
            message = message.format("copied")
    except Exception as e:
        message = "{}".format(e)
        success = False

    return DepResponse(success, message)

def install_link(source, target):
    return install_file(source, target, True)

        
