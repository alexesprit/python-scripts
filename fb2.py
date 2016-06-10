# coding: utf-8

import os
import sys

from argparse import ArgumentParser
from xml.dom import minidom
from xml.parsers.expat import ExpatError


BOOK_AUTHOR = 1
BOOK_TITLE = 2


def normalize_path(fpath):
    return ''.join(char for char in fpath if char not in "\/:*?<>|\"")


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


def get_book_info(book_filename):
    try:
        xmldoc = minidom.parse(book_filename)

        author_tag = xmldoc.getElementsByTagName('author')[0]
        f_name = get_tag_value(author_tag, 'first-name')
        m_name = get_tag_value(author_tag, 'middle-name')
        l_name = get_tag_value(author_tag, 'last-name')

        book_author = ' '.join((
            i.strip() for i in (f_name, m_name, l_name) if i))
        book_title = get_tag_value(xmldoc, 'book-title')

        return {
            BOOK_AUTHOR: book_author,
            BOOK_TITLE: book_title,
        }
    except ExpatError:
        return None


def get_book_filename(book_filename, short=False):
    book_info = get_book_info(book_filename)
    if not book_info:
        return False

    book_title = book_info[BOOK_TITLE]
    if short:
        new_filename = book_title
    else:
        book_author = book_info[BOOK_AUTHOR]
        new_filename = '{0} - {1}'.format(book_author, book_title)

    new_filename = normalize_path(new_filename)
    file_extension = os.path.splitext(book_filename)[1]
    return '{0}{1}'.format(new_filename, file_extension)


def rename_book(book_filename, short=False):
    new_filename = get_book_filename(book_filename, short)
    if new_filename != book_filename:
        os.rename(book_filename, new_filename)
    return True


def create_arg_parser():
    parser = ArgumentParser(
        prog='fb2',
        description='Rename book filenames.')
    parser.add_argument(dest='book',
                        help='Book filename or directory with books')
    parser.add_argument('-s', '--short', default=False, action='store_true',
                        help='Use book title only as filename')
    return parser


def parse_args(arg_parser):
    args = arg_parser.parse_args()

    if os.path.isfile(args.book):
        if rename_book(args.book, args.short):
            print('Renamed: {0}'.format(args.book))
        else:
            print('Cannot rename {0}'.format(args.book))
        return 0
    elif os.path.isdir(args.book):
        for book_filename in gen_book_files(args.book):
            if rename_book(book_filename, args.short):
                print('Renamed: {0}'.format(book_filename))
            else:
                print('Cannot rename {0}'.format(book_filename))
        return 0
    else:
        arg_parser.error('{0} does not exist'.format(args.book))
        return 2


def main():
    arg_parser = create_arg_parser()
    return parse_args(arg_parser)


if '__main__' == __name__:
    sys.exit(main())
