from abc import ABCMeta, abstractmethod

class Shell:
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def execute(args): raise NotImplementedError()