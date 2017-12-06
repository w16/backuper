from abc import ABCMeta, abstractmethod
import hashlib

BUF_LEN = 131072

class CompressionMethod:
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def compress(input_file, output_file): raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def extract(input_file, output_file): raise NotImplementedError()

    @staticmethod
    def checksum(input_file):
        sha256 = hashlib.sha256()
        with open(input_file, 'rb') as fp:
            while True:
                buf = fp.read(BUF_LEN)
                if len(buf) <= 0:
                    break
                sha256.update(buf)
        return sha256.hexdigest()
            