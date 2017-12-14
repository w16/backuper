from abc import ABCMeta, abstractmethod

class Shell:
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, args): raise NotImplementedError()