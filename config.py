import json

from paramiko import SSHClient

from compression.targz import TarGz

from database.sql.mysql import MySQLDumper
from database.sql.postgresql import PostgreSQLDumper

from filesystem.local import LocalFileSystem
from filesystem.remote.ftp import FTPFileSystem
from filesystem.remote.sftp import SFTPFileSystem

from shell.local import SystemShell
from shell.remote.ssh import SSH

from storage.aws_s3 import S3

class AppConfiguration(object):
    def __init__(self, config_json='config.json'):
        with open(config_json, 'r') as config:
            self.config = json.load(config)

    def _get_app_by_id(self, app_id):
        app = filter(lambda x: x['id'] == app_id, self.config['applications'])[0]
        if not app:
            raise AttributeError('Application ID not found on configuration JSON file!')

        return app

    def applications(self):
        return map(lambda x: x['id'], self.config['applications'])

    def compression(self, app_id):
        app = self._get_app_by_id(app_id)
        compression_method = app['compression']['type']

        if compression_method == 'targz':
            return TarGz
        else:
            raise AttributeError('Invalid compression type')

    def database_dumper(self, app_id):
        app = self._get_app_by_id(app_id)
        database = app['database']

        if database['type'] == 'mysql':
            return MySQLDumper(
                database['name'],
                database['username'],
                database['password'],
                database['host'],
                database['port'],
                database['shell']
            )
        elif database['type'] == 'postgresql':
            return PostgreSQLDumper(
                database['name'],
                database['username'],
                database['password'],
                database['host'],
                database['port'],
                database['shell']
            )
        else:
            raise AttributeError('Invalid database type')
    
    def filesystem(self, app_id, channel=None):
        app = self._get_app_by_id(app_id)
        filesystem = app['filesystem']

        if filesystem['type'] == 'local':
            fs = LocalFileSystem()
            fs.cd(filesystem['path'])
            return fs
        elif filesystem['type'] == 'ftp':
            return FTPFileSystem(
                filesystem['host'],
                filesystem['user'],
                filesystem['password'],
                filesystem['port'],
                tmp=app['tmp_dir']
            )
        elif filesystem['type'] == 'sftp':
            if not channel or not isinstance(channel, SSHClient):
                raise AttributeError('SFTP needs a SSH channel and none was provided')

            return SFTPFileSystem(channel)
        else:
            raise AttributeError('Invalid FileSystem type')

    def shell(self, app_id):
        app = self._get_app_by_id(app_id)
        shell = app['shell']

        if shell['type'] == 'system':
            return SystemShell()
        elif shell['type'] == 'ssh':
            return SSH(
                shell['host'],
                shell['username'],
                shell['password'],
                shell['port']
            )
        else:
            raise AttributeError('Invalid shell type')

    def storage(self, app_id):
        app = self._get_app_by_id(app_id)
        storage = app['storage']

        s3_config = app['s3']

        if storage['type'] == 's3':
            return S3(
                s3_config['region'],
                s3_config['key'],
                s3_config['secret'],
                s3_config['bucket'],
            )