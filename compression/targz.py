from compression.compression import CompressionMethod
import tarfile
import os

class TarGz(CompressionMethod):
    def compress(input_file, output_file):
        with tarfile.open(output_file, 'w:gz') as tar:
            tar.add(input_file, arcname=os.path.basename(input_file))

    def extract(input_file, output_file):
        with tarfile.open(input_file, 'r:gz') as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar)
