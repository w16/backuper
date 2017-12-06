from database.database import Database
import os

class MySQLDumper(Database):
    def __init__(self, database, username, password, host, port):
        super().__init__(database, username, password, host, port)
    
    def dump(self, filename):
        if not os.path.isdir(os.path.dirname(filename)):
            os.mkdir(os.path.dirname(filename))

        self.shell.execute([
            'mysqldump',
            '-u{}'.format(self.username),
            '-p{}'.format(self.password),
            self.database,
            '--result-file={}'.format(filename)
        ])

