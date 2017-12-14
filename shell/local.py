import subprocess

from shell import Shell

class SystemShell(Shell):
    def execute(self, args):
        return subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True
        ).communicate()


