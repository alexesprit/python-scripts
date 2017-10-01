# coding: utf-8

import os
import sys

# Append spec "СП" prefix to spec files.
# Usage:
# > spec DIR_NAME


def rename_file(path):
    abs_path = os.path.abspath(path)
    dir_name = os.path.dirname(abs_path)
    base_name = os.path.basename(abs_path)
    file_name, file_ext = os.path.splitext(base_name)

    new_file_name = '{0} СП{1}'.format(file_name, file_ext)
    new_file_path = os.path.join(dir_name, new_file_name)

    os.rename(path, new_file_path)
    print('Renamed {0} to {1}'.format(base_name, new_file_name))


def is_spec_file(file_name):
    file_name = os.path.splitext(file_name)[0]
    return file_name.endswith('.00')


def main(argv):
    dir_path = argv[1]

    for root, _, files in os.walk(dir_path):
        for f in files:
            if is_spec_file(f):
                path = os.path.join(root, f)
                rename_file(path)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
