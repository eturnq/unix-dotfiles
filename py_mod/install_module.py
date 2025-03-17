from json import loads as load_json
from pathlib import Path as FsItem
import subprocess

from py_mod.install_dep import install_archive, install_file, install_link # type: ignore
from py_mod.install_dep import install_package # type: ignore

def manifest_is_valid(manifest):
    return "module" in manifest and "items" in manifest["module"] and "dependencies" in manifest["module"]

def read_manifest_file(filename):
    try:
        with open(filename, "r") as file:
            m = load_json(file.read())
            return m if manifest_is_valid(m) else None
    except Exception as e:
        _ = e 
        return None
    
def dir_is_module(dir):
    return read_manifest_file(dir / "manifest.json") is not None

class ModuleItem:
    _install_types = [ "link", "copy", "extract" ]

    def __init__(self, path, item_dict):
        self._path = path

        if "src" in item_dict:
            self._src = item_dict["src"]
        else:
            self._src = None 

        if "dst" in item_dict:
            self._dst = item_dict["dst"]
        else:
            self._dst = None

        if "install_type" in item_dict and item_dict["install_type"] in self._install_types:
            self._inst = item_dict["install_type"]
        else:
            self._inst = "copy"

    def is_valid(self):
        return self._src is not None and self._dst is not None

    def source(self):
        return self._src

    def destination(self):
        return self._dst

    def install_type(self):
        return self._inst

    def do_install(self):
        if not self.is_valid():
            print("Item is not valid")
            return False

        if self._inst == "copy":
            print("Full install {} to {}...".format(self._src, self._dst))
            return install_file(str(self._path / self._src), self._dst)
        elif self._inst == "link":
            print("Linking {} to {}...".format(self._src, self._dst))
            return install_link(str(self._path / self._src), self._dst)
        else:
            print("Extracting {} to {}...".format(self._src, self._dst))
            return install_archive(str(self._path / self._src), self._dst)

def is_item_in_module(module, item):
    return module is not None and "module" in module and item in module["module"]

def get_module_item(module, item):
    return module["module"][item] if is_item_in_module(module, item) else None

class Module:
    def __init__(self, path: FsItem):
        self._manifest = read_manifest_file(path / "manifest.json")
        self._path = path

        items = [ModuleItem(path, item) for item in self._manifest["module"]["items"]] if self._manifest is not None else []
        self._items = list(filter(lambda item: item.is_valid(), items))

        self._preInst = get_module_item(self._manifest, "preInstallScripts")
        self._postInst = get_module_item(self._manifest, "postInstallScripts")

    def is_valid(self):
        return self._manifest is not None and manifest_is_valid(self._manifest)

    def path(self):
        return self._path

    def name(self):
        if self.is_valid(): # self._manifest can't be None if valid
            return self._manifest["module"]["name"] # type: ignore
        return None

    def items(self):
        return self._items

    def dependencies(self):
        if self.is_valid(): # self._manifest can't be None if valid
            return self._manifest["module"]["dependencies"] # type: ignore
        return []

    def preInstallScripts(self):
        return self._preInst if self._preInst is not None else []

    def postInstallScripts(self):
        return self._postInst if self._postInst is not None else []

    def do_install(self):
        if not self.is_valid():
            print("Module is not valid")
            return False

        print("Installing module {}...".format(self.name()))

        for cmd in self.preInstallScripts():
            subprocess.run([str(self._path / cmd)])

        print("Installing dependencies...")
        if not install_package(self.dependencies()).success:
            return False

        for item in self._items:
            if not item.do_install():
                return False
        
        for cmd in self.postInstallScripts():
            subprocess.run([str(self._path / cmd)])

        return True
    
def get_modules():
    thisdir = FsItem(".").resolve().iterdir()
    childdirs = [child for child in thisdir if child.is_dir()]
    raw_modules = [Module(child) for child in childdirs]
    return [child for child in raw_modules if child.is_valid()]
