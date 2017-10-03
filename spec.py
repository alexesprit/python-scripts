# coding: utf-8

import os
import sys
from argparse import ArgumentParser


def rename_file(path, dry_run=False):
    abs_path = os.path.abspath(path)
    dir_name = os.path.dirname(abs_path)
    base_name = os.path.basename(abs_path)
    file_name, file_ext = os.path.splitext(base_name)

    new_file_name = '{0} СП{1}'.format(file_name, file_ext)
    new_file_path = os.path.join(dir_name, new_file_name)

    if not dry_run:
        try:
            os.rename(path, new_file_path)
        except OSError:
            print('Unable to rename {0}'.format(base_name))
            return
    print('Renamed {0} to {1}'.format(base_name, new_file_name))


def is_spec_file(file_name):
    file_name = os.path.splitext(file_name)[0]
    return file_name.endswith('.00')


def create_arg_parser():
    parser = ArgumentParser(
        prog='spec',
        description='Append spec "СП" prefix to spec files.')
    parser.add_argument(dest='dirs', nargs='+', help='Target directory')
    parser.add_argument('--dry-run', default=False, action='store_true',
                        help='Do not rename files')
    return parser


def parse_args(arg_parser):
    args = arg_parser.parse_args()

    for d in args.dirs:
        for root, _, files in os.walk(d):
            for f in files:
                if is_spec_file(f):
                    path = os.path.join(root, f)
                    rename_file(path, args.dry_run)
    return 0


def main():
    arg_parser = create_arg_parser()
    return parse_args(arg_parser)


if __name__ == '__main__':
    sys.exit(main())
