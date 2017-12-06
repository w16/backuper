import subprocess

from shell.shell import Shell

class SystemShell(Shell):

    @staticmethod
    def execute(args):
        return subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ).communicate()


