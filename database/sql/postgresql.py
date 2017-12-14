from database import Database

class PostgreSQLDumper(Database):
    def __init__(self, database, username, password, host, port, shell):
        super().__init__(database, username, password, host, port, shell)

    def dump(self, output_file):
        self.shell.execute(
            'pg_dump -h {} -p {} -U {} -W {} -Fc {} -f {}'.format(
                self.host,
                self.port,
                self.username,
                self.password,
                self.database,
                output_file
            )
        )