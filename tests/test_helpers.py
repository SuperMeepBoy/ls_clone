from tempfile import mkdtemp
from unittest.mock import patch, MagicMock
from shutil import rmtree
import env
import os

import pytest

from src.helpers import count_files, count_lines, scantree
from tools import PseudoDirEntry, create_tmp_file


class TestHelpers:

    def test_count_lines_file(self):
        try:
            content = """Hello world
            How are
            you ?"""
            tmp_file = create_tmp_file(content=content)
            tmp_dir_entry = PseudoDirEntry(tmp_file.name, tmp_file.name)
            assert count_lines(tmp_dir_entry) == '3'
        finally:
            os.remove(tmp_file.name)

    def test_count_lines_dir(self):
        try:
            tmp_dir = mkdtemp()
            tmp_dir_entry = PseudoDirEntry(tmp_dir, tmp_dir, 'dir')
            assert count_lines(tmp_dir_entry) == '-'
        finally:
            os.rmdir(tmp_dir)

    def test_count_files(self):
        try:
            tmp_dir = mkdtemp()
            tmp_dir_dir_entry = PseudoDirEntry(tmp_dir, tmp_dir, 'dir')
            tmp_hidden_file = create_tmp_file(dir=tmp_dir)
            tmp_not_hidden_file = create_tmp_file(dir=tmp_dir, prefix='.')
            tmp_hidden_file_dir_entry = PseudoDirEntry(tmp_hidden_file, tmp_hidden_file.name)
            assert count_files(tmp_dir_dir_entry, hide_hidden=False) == '2'
            assert count_files(tmp_dir_dir_entry, hide_hidden=True) == '1'
            assert count_files(tmp_hidden_file_dir_entry) == '-'
        finally:
            os.remove(tmp_hidden_file.name)
            os.remove(tmp_not_hidden_file.name)
            os.rmdir(tmp_dir)

    def test_scantree_hide_hidden(self):
        # root
        # |_hidden_dir
        # | |_hidden_file
        # | |_not_hidden_file
        # |_not_hidden_dir *
        # | |_hidden_file *
        # | |_not_hidden_file
        # |_hidden_file
        # |_not_hidden_file *
        try:
            root = mkdtemp()
            hidden_dir = mkdtemp(prefix='.', dir=root)
            not_hidden_dir = mkdtemp(dir=root)
            directories = [root, hidden_dir, not_hidden_dir]
            fileslist = []
            for directory in directories:
                fileslist.append(create_tmp_file(dir=directory))
                fileslist.append(create_tmp_file(prefix='.', dir=directory))
            result = scantree(root)
            result_list = [f.name for f in result]
            assert len(result_list) == 3
            for r in result_list:
                assert not r.startswith('.')
        finally:
            rmtree(root)

    def test_scantree_show_hidden(self):
        # root
        # |_hidden_dir *
        # | |_hidden_file *
        # | |_not_hidden_file *
        # |_not_hidden_dir *
        # | |_hidden_file *
        # | |_not_hidden_file *
        # |_hidden_file *
        # |_not_hidden_file *
        try:
            root = mkdtemp()
            hidden_dir = mkdtemp(prefix='.', dir=root)
            not_hidden_dir = mkdtemp(dir=root)
            directories = [root, hidden_dir, not_hidden_dir]
            fileslist = []
            for directory in directories:
                fileslist.append(create_tmp_file(dir=directory))
                fileslist.append(create_tmp_file(prefix='.', dir=directory))
            result = scantree(root, False)
            result_list = [f.name for f in result]
            assert len(result_list) == 8
        finally:
            rmtree(root)
