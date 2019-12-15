# coding: utf-8

import os
import sys
from argparse import ArgumentParser

def remove_spec_suffix(name):
    # todo smart skip
    return name[0:-3]

def get_assembly(path):
    base_name = os.path.basename(path)
    file_name, _ = os.path.splitext(base_name)

    return remove_spec_suffix(file_name)

def make_dir_for_assembly(path, dry_run=False):
    file_dir = os.path.dirname(path)

    assembly_name = get_assembly(path)
    assembly_path = os.path.join(file_dir, assembly_name)

    if not os.path.isdir(assembly_path):
        if not dry_run:
            os.mkdir(assembly_path)
        print('Made directory for {assembly_name}')
    else:
        print(f'Skip directory for {assembly_name}, already exists')

def is_spec_file(file_name):
    file_name = os.path.splitext(file_name)[0]
    return file_name.endswith(' СП')

def create_arg_parser():
    parser = ArgumentParser(
        prog='asmkd',
        description='Make subdirs for assemblies.')
    parser.add_argument(dest='dirs', nargs='+', help='Target directory')
    parser.add_argument('--dry-run', default=False, action='store_true',
                        help='Do not make directories')
    return parser


def parse_args(arg_parser):
    args = arg_parser.parse_args()

    for d in args.dirs:
        for _, _, files in os.walk(d):
            for f in files:
                if is_spec_file(f):
                    make_dir_for_assembly(f)
    return 0


def main():
    arg_parser = create_arg_parser()
    return parse_args(arg_parser)


if __name__ == '__main__':
    sys.exit(main())
