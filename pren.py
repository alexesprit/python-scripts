# coding: utf-8

import os
import re
import sys
from argparse import ArgumentParser

PROGRAM_RE = re.compile(r'Задание\s(\w+)\sраскрой\s\d+\.iso')


def rename_file(path, dry_run=False):
    abs_path = os.path.abspath(path)
    dir_name = os.path.dirname(abs_path)
    base_name = os.path.basename(abs_path)
    _, file_ext = os.path.splitext(base_name)

    program_name = PROGRAM_RE.search(base_name).group(1)

    new_file_name = f'{program_name}{file_ext}'
    new_file_path = os.path.join(dir_name, new_file_name)

    if not dry_run:
        try:
            os.rename(path, new_file_path)
        except OSError:
            print(f'Unable to rename {base_name}')
            return
    print(f'Renamed {base_name} to {new_file_name}')


def is_program(file_name):
    return PROGRAM_RE.match(file_name)


def create_arg_parser():
    parser = ArgumentParser(
        prog='pren',
        description='Rename programs.')
    parser.add_argument(dest='dirs', nargs='+', help='Target directory')
    parser.add_argument('--dry-run', default=False, action='store_true',
                        help='Do not rename files')
    return parser


def parse_args(arg_parser):
    args = arg_parser.parse_args()

    for d in args.dirs:
        for _, _, files in os.walk(d):
            for f in files:
                if is_program(f):
                    rename_file(f, args.dry_run)
    return 0


def main():
    arg_parser = create_arg_parser()
    return parse_args(arg_parser)


if __name__ == '__main__':
    sys.exit(main())
