#!/usr/bin/python3
"""ls.

Usage:
  main.py [-a] [-R] [-l] [-c] [-d] [-r] [-S] [<file>]
  main.py -h | --help
  main.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

  -a            Include hidden files.
  -R            Recursive search.
  -l            Display files size.
  -c            Display files number of lines.
  -d            Only display folders and number of files within them.
  -r            Reverse display order.
  -S            Sort by size.
"""

from operator import itemgetter
import os

from docopt import docopt

import helpers


class Ls:

    def __init__(self, arguments):
        self.filename = arguments.get('<file>', '.')
        self.recursive = arguments.get('-R', False)
        self.only_dirs_and_files_number = arguments.get('-d', False)
        self.hide_hidden = not arguments.get('-a', False)
        self.display_number_of_lines = arguments.get('-c', False)
        self.display_size = arguments.get('-l', False)
        self.sort_mode = 'size' if arguments.get('-S') else 'path'
        self.reverse_display = arguments.get('-r', False)

    def run(self):
        self.compute_ls()
        self.display_ls()

    def compute_ls(self):
        if self.recursive:
            self.scan = list(helpers.scantree(self.filename, self.hide_hidden))
        else:
            self.scan = list(os.scandir(self.filename))
            if self.hide_hidden:
                self.scan = [filename for filename in self.scan
                             if not filename.name.startswith('.')]

        if self.only_dirs_and_files_number:
            self.scan = [filename for filename in self.scan
                         if filename.is_dir()]

    def display_ls(self):
        infos = {}
        for filename in self.scan:
            infos[filename] = dict(path=filename.path)
            if self.display_size:
                infos[filename]['size'] = str(filename.stat().st_size)
            if self.display_number_of_lines:
                infos[filename]['lines'] = helpers.count_lines(filename)
            if self.only_dirs_and_files_number:
                infos[filename]['files'] = helpers.count_files(filename,
                                                       self.hide_hidden)
        infos = sorted(infos.values(),
                       key=itemgetter(self.sort_mode),
                       reverse=self.reverse_display,)
        first_line = True
        for info in infos:
            if first_line:
                print(' '.join(info.keys()))
            first_line = False
            print(' '.join(info.values()))


if __name__ == '__main__':
    arguments = docopt(__doc__, version='ls 0.1.0')
    Ls(arguments).run()
