from compression.compression import CompressionMethod
import tarfile
import os

class TarGz(CompressionMethod):
    def compress(input_file, output_file):
        with tarfile.open(output_file, 'w:gz') as tar:
            tar.add(input_file, arcname=os.path.basename(input_file))

    def extract(input_file, output_file):
        with tarfile.open(input_file, 'r:gz') as tar:
            tar.extractall()
