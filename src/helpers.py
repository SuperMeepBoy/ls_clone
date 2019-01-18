import os

def scantree(path, hide_hidden=True):
    if path.startswith('.') and not hide_hidden:
        yield
    for entry in os.scandir(path):
        if entry.name.startswith('.') and hide_hidden:
            continue
        else:
            yield entry
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path, hide_hidden)

def count_files(filename, hide_hidden=False):
    if not filename.is_dir():
        return '-'
    files = [name for name in os.listdir(filename.path)
             if os.path.isfile(os.path.join(filename.path, name))]
    if hide_hidden:
        files = [name for name in files if not name.startswith('.')]
    return str(len(files))

def count_lines(filename):
    # Right encoding : https://stackoverflow.com/questions/19699367/unicodedecodeerror-utf-8-codec-cant-decode-byte
    return (str(sum(1 for line in open(filename.path, encoding="ISO-8859-1")))
            if filename.is_file() else '-')
