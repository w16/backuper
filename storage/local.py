import os
from storage import Storage

class LocalStorage(Storage):
    def __init__(self, path):
        self.path = path

    def read(self, filename, mode='rb'):
        return open(filename, mode).read()

    def write(self, filename, mode='wb', output=None):
        output_file = output
        if not output_file:
            output_file = os.path.basename(filename)
        
        output_file = os.path.join(self.path, output_file)

        with open(filename, 'rb') as input_file:
            with open(output_file, mode) as out:
                out.write(input_file.read())