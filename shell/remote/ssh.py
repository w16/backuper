from shell import Shell
from paramiko import SSHClient, AutoAddPolicy

class SSH(Shell):
    def __init__(self, host, username, password, port):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self._channel = None

    def _connect(self):
        self._channel = SSHClient()
        self._channel.load_system_host_keys()
        self._channel.set_missing_host_key_policy(AutoAddPolicy)
        self._channel.connect(
           self.host,
           port=self.port,
           username=self.username,
           password=self.password
        )

    def channel(self):
        if not self._channel:
            self._connect()
        return self._channel

    def execute(self, args):
        if not self._channel:
            self._connect()
       return self._channel.exec_command(args)