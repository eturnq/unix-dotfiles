import subprocess

from pathlib import Path as FsItem
from shutil  import copyfile
import subprocess

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
        _ = fs_item.lstat()
        return True
    except Exception as e:
        _ = e
        return False

def install_file(source, target, is_link=False):
    success = True
    message = "{} {} to {}".format("{}", source, target)


    src = FsItem(source).expanduser().resolve() # DO resolve symlinks
    tgt = FsItem(target).expanduser() # Do NOT resolve symlinks

    if not src.exists():
        return DepResponse(False, "{} doesn't exist".format(source))

    if fs_item_exists(tgt):
        print("Target {} exists".format(target))
        user_input = input("Overwrite? (yes/no[default]): ").lower()
        is_affirm = user_input == "yes" or user_input == "y"
        if not is_affirm: return DepResponse(True, "Not overwriting target")

        tgt.unlink(missing_ok=True)

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
    print("Entering install_link...")
    return install_file(source, target, True)

def install_archive(source, target):
    _ = source 
    _ = target
    print("Unimplemented")
    return False

pkg_name = {
    "apt-get": {
        "command": "sudo {} install -y {}",
        "build-essential": "build-essential",
        "cmake": "cmake",
        "fvwm": "fvwm3",
        "git": "git",
        "tmux": "tmux",
        "unzip": "unzip",
        "wget": "wget",
        "xinit": "xinit",
        "xterm": "xterm",
        "zsh": "zsh"
    }
}

def get_package_manager():
    supported = list(pkg_name.keys())
    return next(filter(lambda pkg: exe_in_path(pkg), supported), None)

def install_package(names):
    pkgmgr = get_package_manager()
    if pkgmgr is None:
        return DepResponse(False, "No supported package manager found.")

    pkg_names = None

    try:
        pkg_names = pkg_name[pkgmgr]
    except Exception as e:
        _ = e
        return DepResponse(False, "No supported package found.")

    pkg_list = list(filter(lambda pkg: pkg in pkg_names.keys(), names))
    pkg_list = [pkg_names[pkg] for pkg in pkg_list]
    full_cmd = pkg_names["command"].format(pkgmgr, " ".join(pkg_list))
    print("Executing \"{}\"".format(full_cmd))
    subprocess.run(full_cmd.split())
    # TODO: capture if install was successful
    return DepResponse(True, "")
