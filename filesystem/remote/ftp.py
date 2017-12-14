from filesystem import FileSystem
from ftplib import FTP

class FTPFileSystem(FileSystem):
    def __init__(self, host, user, password, port=21, tmp='/tmp/backuper'):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    def __enter__(self):
        self.ftp = FTP(self.host, self.username, self.password)
        return self

    def __exit__(self);
        self.ftp.quit()
    
    def cd(self, path):
        self.ftp.cwd(path)

    def mkdir(self, name):
        self.ftp.mkd(name)

    def cp(self, src, dst): raise NotImplementedError()

    def mv(self, src, dst): raise NotImplementedError()

    def rm(self, name):
        self.ftp.delete(name)

    def cwd(self, name):
        return self.ftp.pwd()

    def ls(self, path=None):
        lst = list(self.ftp.mlsd())
        return map(lambda x: x[0], lst)

    def open(self, path, mode='r'):
        tmp = '{}/{}'.format(self.tmp, path)
        self.ftp.retrbinary('RETR {}'.format(path), open(tmp, 'wb').write)
        return open(tmp, mode)