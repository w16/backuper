from abc import ABCMeta, abstractmethod

class FileSystem:
    __metaclass__ = ABCMeta

    @abstractmethod
    def cd(self, path): raise NotImplementedError()

    @abstractmethod
    def mkdir(self, name): raise NotImplementedError()

    @abstractmethod
    def cp(self, src, dst): raise NotImplementedError()

    @abstractmethod
    def mv(self, src, dst): raise NotImplementedError()

    @abstractmethod
    def rm(self, name): raise NotImplementedError()

    @abstractmethod
    def cwd(self, name): raise NotImplementedError()

    @abstractmethod
    def ls(self, path=None): raise NotImplementedError()

    @abstractmethod
    def open(self, path, mode="r"): raise NotImplementedError()