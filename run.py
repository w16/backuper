import json
import time
import os
import glob
import logging

from database.sql.mysql import MySQLDumper
from compression.targz import TarGz
from storage.aws_s3 import S3

logger = logging.getLogger()

def main():
    with open('config.json', 'r') as config_file:
        logger.debug("Loading config.json file...")
        config = json.load(config_file)
        logger.info("config.json loaded!")

        logger.debug("Initializing AWS S3 connection...")
        fs = S3(
            config['storage']['region'],
            config['storage']['key'],
            config['storage']['secret'],
            config['storage']['bucket'],
        )
        logger.info("S3 connection estabilished!")

        logger.debug("Getting applications from config file...")
        for app in config['applications']:
            logger.info("Starting backup process of {}".format(app['name']))
            stamp = time.strftime('%Y%m%d-%H%M%S')
            filename = app['id'] + '-' + stamp

            db_dumper = MySQLDumper(
                app['database']['name'],
                app['database']['username'],
                app['database']['password'],
                app['database']['host'],
                app['database']['port']
            )
            
            logger.info("Dumping '{}' database".format(app['database']['name']))
            db_dumper.dump('/tmp/backuper/{}.sql'.format(filename))
            logger.info("Database dumped to /tmp/backuper/{}.sql".format(filename))

            logger.info("Compressing dump file")
            TarGz.compress(
                '/tmp/backuper/{}.sql'.format(filename),
                '/tmp/backuper/{}.sql.tar.gz'.format(filename)
            )
            logger.info(
                "Dump file '/tmp/backuper/{}.sql.tar.gz' compressed \
                using gzip".format(filename)
            )

            logger.info("Compressing application files")
            TarGz.compress(
                app['path'],
                '/tmp/backuper/{}.tar.gz'.format(filename)
            )
            logger.info(
                "File '/tmp/backuper/{}.tar.gz' compressed".format(filename)
            )

            logger.info("Sending database dump backup to storage")
            fs.write(
                '/tmp/backuper/{}.sql.tar.gz'.format(filename),
                output='{}/{}/{}.sql.tar.gz'.format(app['id'], stamp, filename)
            )

            logger.info("Sending application files backup to storage")
            fs.write(
                '/tmp/backuper/{}.tar.gz'.format(filename),
                output='{}/{}/{}.tar.gz'.format(app['id'], stamp, filename)
            )
            
            logger.info("Removing temporary files")
            map(os.remove, glob.glob('/tmp/backuper/{}*'.format(filename)))

            logger.info("Backup of {} is done".format(app['name']))

    logger.info("Done")


if __name__ == '__main__':
    main()