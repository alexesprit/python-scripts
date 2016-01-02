# coding: utf-8

from __future__ import unicode_literals

import os
import sys

from xml.dom import minidom
from xml.parsers.expat import ExpatError


def normalize_path(fpath):
    return ''.join(char for char in fpath if char not in '\\/:*?<>|"')


def is_book(filename):
    extension = os.path.splitext(filename)[1]
    return extension == '.fb2'


def gen_book_files(directory):
    for root, dirs, files in os.walk(directory):
        for fn in files:
            if is_book(fn):
                yield os.path.join(root, fn)


def get_tag_value(xmldoc, tagname):
    tags = xmldoc.getElementsByTagName(tagname)
    if tags:
        tag = tags[0]
        tagdata = []
        for child in tag.childNodes:
            if child.nodeType == minidom.Node.TEXT_NODE:
                tagdata.append(child.data)
        return ''.join(tagdata)
    return None


def rename_book(path):
    try:
        xmldoc = minidom.parse(path)
        book_title = get_tag_value(xmldoc, 'book-title')
        first_name = get_tag_value(xmldoc, 'first-name')
        last_name = get_tag_value(xmldoc, 'last-name')
    except ExpatError:
        print(path)
        return False

    author_name = ' '.join(
        filter(None, (first_name, last_name))
    )
    new_fn = '{0} - {1}.fb2'.format(author_name, book_title)
    new_fn = normalize_path(new_fn)
    new_path = os.path.join(os.path.dirname(path), new_fn)

    if new_path != path:
        try:
            os.rename(path, new_path)
            return True
        except WindowsError:
            print(path)

    return False


def rename_books(directory):
    counter = 0
    for f in gen_book_files(directory):
        if rename_book(f):
            counter += 1
    if counter:
        print('Renamed {0} files'.format(counter))
    else:
        print('No files are renamed')


def main(args):
    path = ''.join(args[1:])
    if os.path.isfile(path):
        rename_book(path)
    elif os.path.isdir(path):
        rename_books(path)
    else:
        print('Unknown file or directory')
    return 0


if '__main__' == __name__:
    sys.exit(main(sys.argv))
