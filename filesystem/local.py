from filesystem import FileSystem
import os
import shutil

class LocalFileSystem(FileSystem):
    def cd(self, path):
        os.chdir(path)

    def mkdir(self, name):
        os.mkdir(name)

    def cp(self, src, dst):
        shutil.copyfile(src, dst)

    def mv(self, src, dst):
        os.rename(src, dst)

    def rm(self, name):
        os.remove(name)

    def cwd(self):
        return os.getcwd()

    def ls(self, path=None):
        real_path = path

        if not path:
            real_path = self.cwd()
        
        return os.listdir(path)

    def open(self, path, mode="r"):
        return open(path, mode)
