import platform
import subprocess

class PackageManager:
    def __init__(self):
        # TODO: get search keyword
        # TODO: get locate? keyword
        match platform.system():
            case "Darwin":
                self.bin = "brew"
                self.install_keyword = "install"
                self.valid = True
            case _:
                self.bin = ""
                self.install_keyword = ""
                self.valid = False

    def install(self, package):
        result = subprocess.run([self.bin, self.install_keyword, package])
        if len(result.stdout) > 0:
            print(result.stdout)
        if len(result.stderr) > 0:
            print(result.stderr)

