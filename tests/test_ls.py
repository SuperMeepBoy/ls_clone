from tempfile import mkdtemp
from unittest.mock import patch, MagicMock
import env
import os

import pytest

from src.main import Ls
from tools import PseudoDirEntry, create_tmp_file


root = mkdtemp()
root_dir_entry = PseudoDirEntry(root, root, 'dir')
dirname = mkdtemp(dir=root)
dirname_dir_entry = PseudoDirEntry(dirname, dirname, 'dir')
file_in_dir = create_tmp_file(dir=dirname)
file_in_dir = PseudoDirEntry(file_in_dir.name, file_in_dir.name)
hidden_dir = mkdtemp(dir=root, prefix='.')
hidden_dir_dir_entry = PseudoDirEntry(hidden_dir, hidden_dir, 'dir')
hidden_file = create_tmp_file(dir=root, prefix='.')
hidden_file_dir_entry = PseudoDirEntry(hidden_file.name, hidden_file.name)
filename = create_tmp_file(dir=root)
filename_dir_entry = PseudoDirEntry(filename.name, filename.name, size=2048)


class TestLs:

    @pytest.mark.parametrize("args,expected_result", [
        ({'<file>': root, }, [dirname, filename.name]),
        ({'<file>': root, '-a': True}, [dirname, filename.name, hidden_file.name, hidden_dir]),
        ({'<file>': root, '-d': True}, [dirname]),
        ({'<file>': root, '-R': True}, [dirname, filename.name, file_in_dir.name]),
        ({'<file>': root, '-a': True, '-d': True}, [hidden_dir, dirname]),
        ({'<file>': root, '-a': True, '-R': True}, [dirname, filename.name, hidden_file.name, hidden_dir, file_in_dir.name]),
        ({'<file>': root, '-d': True, '-R': True}, [dirname]),
        ({'<file>': root, '-a': True, '-d': True, '-R': True}, [dirname, hidden_dir]),
    ])
    def test_compute_ls(self, args, expected_result):
        ls = Ls(args)
        ls.compute_ls()
        result = [f.path for f in list(ls.scan)]
        assert set(result) == set(expected_result)

    @patch('os.scandir')
    def test_display_size(self, m_scandir, capsys):
        tmp_file = create_tmp_file(size=1024)
        tmp_file_dir_entry = PseudoDirEntry(tmp_file.name, tmp_file.name)
        m_scandir.return_value = [tmp_file_dir_entry]
        args = {'-l': True}
        ls = Ls(args).run()
        out, err = capsys.readouterr()
        assert out == """path size
{} 1024
""".format(tmp_file_dir_entry.path)

    @patch('os.scandir')
    def test_display_lines(self, m_scandir, capsys):
        tmp_file = create_tmp_file(content="""Beware the Jabberwock, my son!
The jaws that bite, the claws that catch!
Beware the Jubjub bird, and shun
The frumious Bandersnatch!
""")
        tmp_file_dir_entry = PseudoDirEntry(tmp_file.name, tmp_file.name)
        m_scandir.return_value = [tmp_file_dir_entry]
        args = {'-c': True}
        ls = Ls(args).run()
        out, err = capsys.readouterr()
        assert out == """path lines
{} 4
""".format(tmp_file_dir_entry.path)

    def test_display_files(self, capsys):
        args = {'-d': True, '<file>': root}
        ls = Ls(args).run()
        out, err = capsys.readouterr()
        assert out == """path files
{} 1
""".format(dirname_dir_entry.path)
