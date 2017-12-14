from filesystem import FileSystem
import stat

class SFTPFileSystem(FileSystem):
    def __init__(self, ssh_channel):
        self.ssh = ssh_channel

    def __enter__(self):
        self.sftp = self.ssh.open_sftp()
        return self

    def __exit__(self):
        self.ssh.close()

    def cd(self, path):
        self.sftp.chdir(path)

    def mkdir(self, name):
        self.sftp.mkdir(name)

    def cp(self, src, dst):
        with self.sftp.open(src, 'r') as r:
            with self.sftp.open(dst, 'w') as w:
                w.write(r.read())

    def mv(self, src, dst):
        self.sftp.rename(src, dst)

    def rm(self, name):
        attrs = self.sftp.stat(name)
        if stat.S_ISDIR(attrs.st_mode):
            self.sftp.rmdir(name)
        else:
            self.sftp.remove(name)
    
    def cwd(self):
        return self.sftp.getcwd()

    def ls(self, path=None):
        if not path:
            path = '.'

        return self.sftp.listdir(path)

    def open(self, path, mode='r'):
        return self.sftp.open(path, mode)


            
