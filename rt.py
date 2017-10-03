# coding: utf-8

# https://wiki.theory.org/Decoding_bencoded_data_with_python

import glob
import os
import re
import sys

decimal_match = re.compile(r'\d')


def bdecode(data):
    chunks = list(data)
    chunks.reverse()
    root = _dechunk(chunks)
    return root


def _dechunk(chunks):
    item = chunks.pop()

    if item == 'd':
        item = chunks.pop()
        hash_data = {}
        while item != 'e':
            chunks.append(item)
            key = _dechunk(chunks)
            hash_data[key] = _dechunk(chunks)
            item = chunks.pop()
        return hash_data
    elif item == 'l':
        item = chunks.pop()
        arr = []
        while item != 'e':
            chunks.append(item)
            arr.append(_dechunk(chunks))
            item = chunks.pop()
        return arr
    elif item == 'i':
        item = chunks.pop()
        num = ''
        while item != 'e':
            num += item
            item = chunks.pop()
        return int(num)
    elif decimal_match.search(item):
        num = ''
        while decimal_match.search(item):
            num += item
            item = chunks.pop()
        line = ''
        for _ in range(int(num)):
            line += chunks.pop()
        return line
    raise IOError("Invalid input")


def rename_file(path):
    raw_data = open(path, 'rb').read()
    metadata = bdecode(raw_data)
    new_path = os.path.join(
        os.path.dirname(path),
        metadata['info']['name'] + '.torrent'
    )
    if path != new_path:
        os.rename(path, new_path)
        return True
    return False


def rename_files_in_dir(path):
    files = glob.glob(os.path.join(path, '*.torrent'))
    if files:
        counter = 0
        for f in files:
            if rename_file(f):
                counter += 1
        if counter:
            print('Renamed {0} files'.format(counter))
        else:
            print('No files are renamed')
    else:
        print('No torrent files in {0}'.format(os.path.abspath(path)))


def main(args):
    path = ''.join(args[1:])
    if os.path.isfile(path):
        rename_file(path)
    elif os.path.isdir(path):
        rename_files_in_dir(path)
    else:
        print(u'Unknown file or directory')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
