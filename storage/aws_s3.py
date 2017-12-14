import boto3
from storage import Storage
from os import path

class S3(Storage):
    def __init__(self, region, key, secret, bucket, tmp_dir='/tmp/backuper'):
        self.region = region
        self.key = key
        self.secret = secret
        self.bucket = bucket
        self.tmp_dir = tmp_dir
        self._connect()

    def _connect(self):
        self.s3_client = boto3.client(
            's3',
            region_name=self.region,
            aws_access_key_id=self.key,
            aws_secret_access_key=self.secret
        )

    def read(self, filename, mode="r"):
        if not self.s3_client:
            self._connect()

        tmp_file = path.join(self.tmp_dir, filename)

        self.s3_client.download_file(self.bucket, filename, tmp_file)
        return open(tmp_file, mode)

    def write(self, filename, mode="w", output=None):
        if not self.s3_client:
            self._connect()

        if not output:
            output = path.basename(filename)

        self.s3_client.upload_file(filename, self.bucket, output)