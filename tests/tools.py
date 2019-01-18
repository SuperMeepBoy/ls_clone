from tempfile import NamedTemporaryFile
from unittest.mock import MagicMock
import os


class PseudoDirEntry:
    def __init__(self, name, path, filetype='file', size=0):
        self.name = name
        self.path = path
        if filetype == 'file':
            self._is_dir = False
            self._is_file = True
        else:
            self._is_dir = True
            self._is_file = False

        self._stat = MagicMock()
        self._stat.st_size = self.get_size() or size

    def is_dir(self):
        return self._is_dir

    def is_file(self):
        return self._is_file

    def stat(self):
        return self._stat

    def get_size(self):
        if os.path.isfile(self.path) or os.path.isdir(self.path):
            return os.path.getsize(self.path)

def create_tmp_file(**kwargs):
    content = kwargs.get('content', '')
    size = kwargs.get('size')
    with NamedTemporaryFile(
        delete=False,
        dir=kwargs.get('dir'),
        prefix=kwargs.get('prefix'),
    ) as tmp_file:
        if size:
            tmp_file.write(os.urandom(size))
        else:
            tmp_file.write(content.encode())
    return tmp_file
