from abc import ABCMeta, abstractmethod

class Storage:
    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self, filename, mode="r"): raise NotImplementedError()

    @abstractmethod
    def write(self, filename, mode="w"): raise NotImplementedError()