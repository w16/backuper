import json

from database.sql.mysql import MySQLDumper
from compression.targz import TarGz
from storage.aws_s3 import S3

def main():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

        db_dumper = MySQLDumper(
            config['applications'][0]['database']['name'],
            config['applications'][0]['database']['username'],
            config['applications'][0]['database']['password'],
            config['applications'][0]['database']['host'],
            config['applications'][0]['database']['port']
        )
        db_dumper.dump('/tmp/backuper/test.sql')
        TarGz.compress('/tmp/backuper/test.sql', '/tmp/backuper/test.sql.tar.gz')

        fs = S3(
            config['storage']['region'],
            config['storage']['key'],
            config['storage']['secret'],
            config['storage']['bucket'],
        )

        fs.write('/tmp/backuper/test.sql.tar.gz')

if __name__ == '__main__':
    main()