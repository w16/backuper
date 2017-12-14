from abc import ABCMeta, abstractmethod
from shell.local import SystemShell

class Database:
    __metaclass__ = ABCMeta

    def __init__(self, database, username, password, host, port, shell=SystemShell):
        self.database = database
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.shell = shell

    @abstractmethod
    def dump(self, output_file): raise NotImplementedError()