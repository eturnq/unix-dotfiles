import subprocess

from pathlib import Path as FsItem
from shutil  import copyfile
import subprocess
import zipfile

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
    src = FsItem(source).expanduser().resolve() # DO resolve symlinks
    tgt = FsItem(target).expanduser().resolve() # DO resolve symlinks

    if not src.exists():
        print("src does not exist")
        return False 

    if src.suffix == ".zip":
        with zipfile.ZipFile(src) as archive:
            for name in archive.namelist():
                with archive.open(name) as file:
                    dst = tgt / name
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    print("Writing to {}".format(dst))
                    dst.write_bytes(file.read())
        return True
    else:
        print("Unsupported archive format.")

    return False

pkg_name = {
    "apt-get": {
        "command": "sudo {} install -y {}",
        "bash": "bash",
        "bash-completion": "bash-completion",
        "build-essential": "build-essential",
        "cmake": "cmake",
        "curl": "curl",
        "dunst": "dunst",
        "fvwm": "fvwm3",
        "git": "git",
        "libnotify": "libnotify-bin libnotify4",
        "lightdm": "lightdm",
        "pam": "libpam0g libpam0g-dev",
        "tar": "tar",
        "tmux": "tmux",
        "unzip": "unzip",
        "wget": "wget",
        "wpagui": "wpagui",
        "x11-xserver-utils": "x11-xserver-utils",
        "xcb": "libx11-xcb1 libx11-xcb-dev",
        "xinit": "xinit",
        "xterm": "xterm",
        "xz": "xz-utils",
        "zsh": "zsh"
    },
    "pkg": {
        "command": "sudo {} install -y {}",
        "bash": "bash",
        "bash-completion": "bash-completion",
        "build-essential": "automake gcc gmake",
        "cmake": "cmake",
        "curl": "curl",
        "dunst": "dunst",
        "fvwm": "fvwm3",
        "git": "git",
        "libnotify": "libnotify",
        "lightdm": "lightdm lightdm-gtk-greeter lightdm-gtk-greeter-settings",
        "pam": "",
        "tar": "gtar",
        "tmux": "tmux",
        "unzip": "unzip",
        "wpagui": "wpa_supplicant_gui",
        "x11-xserver-utils": "xorg xorg-apps",
        "xcb": "xcb libxcb",
        "xinit": "xinit",
        "xterm": "xterm",
        "xz": "",
        "zsh": "zsh"
    },
    "xbps-install": {
        "command": "sudo {} -Sy {}",
        "bash": "bash",
        "bash-completion": "bash-completion",
        "build-essential": "automake gcc gettext make",
        "cmake": "cmake",
        "curl": "curl",
        "dunst": "dunst",
        "fvwm": "fvwm3",
        "git": "git",
        "libnotify": "libnotify",
        "lightdm": "lightdm",
        "pam": "pam pam-devel",
        "tar": "tar",
        "tmux": "tmux",
        "unzip": "unzip",
        "wget": "wget",
        "wpagui": "wpa_gui",
        "x11-xserver-utils": "xorg xrdb",
        "xcb": "libxcb libxcb-devel",
        "xinit": "xinit",
        "xterm": "xterm",
        "xz": "xz",
        "zsh": "zsh"
    }
}

def get_package_manager():
    supported = list(pkg_name.keys())
    return next(filter(lambda pkg: exe_in_path(pkg).success, supported), None)

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
