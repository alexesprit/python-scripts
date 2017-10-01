import os
import sys
from argparse import ArgumentParser

CUSTOM_PATHEXT = ('.py', '.lua', '.rb')


def is_executable(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program, show_all):
    fpath, _ = os.path.split(program)
    if fpath and is_executable(program):
        return [program]
    else:
        name, ext = os.path.splitext(program)
        if not ext:
            pathext = os.environ['PathExt'].lower().split(os.pathsep)
            pathext.extend(CUSTOM_PATHEXT)
            pathext = set(pathext)
        else:
            pathext = [ext]

        exe_files = []

        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, name)
            for ext in pathext:
                exe_path = '{0}{1}'.format(exe_file, ext)
                if is_executable(exe_path):
                    if not show_all:
                        return [exe_path]
                    exe_files.append(exe_path)
        return exe_files

    return []


def create_arg_parser():
    parser = ArgumentParser(
        prog='which',
        description='Write the full path of PROGRAM(s) to standard output.')
    parser.add_argument(dest='program', nargs='+', help='Programs to search')
    parser.add_argument('-a', '--all', default=False, action='store_true',
                        help='Print all matches in PATH, not just the first')
    return parser


def parse_args(arg_parser):
    args = arg_parser.parse_args()

    for program in args.program:
        programs = which(program, args.all)
        if programs:
            for program_path in programs:
                print(program_path)
        else:
            print('{0}: not found'.format(program))
    return 0


def main():
    arg_parser = create_arg_parser()
    return parse_args(arg_parser)


if __name__ == '__main__':
    sys.exit(main())
