import os
import sys


def is_executable(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program):
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        extension = os.path.splitext(program)[1]
        pathext = os.environ['PathExt'].lower().split(os.pathsep)

        for path in os.environ['PATH'].split(os.pathsep):
            exe_files = []
            if not extension:
                for ext in pathext:
                    exe_file = os.path.join(path, '{0}{1}'.format(program, ext))
                    exe_files.append(exe_file)
            else:
                exe_files = [os.path.join(path, program)]

            for exe_file in exe_files:
                if is_executable(exe_file):
                    return exe_file

    return None


def main(args):
    program = ''.join(args[1:])
    program_path = which(program)
    if program_path:
        print(program_path)
    else:
        print('{0}: not found'.format(program))
    return 0


if '__main__' == __name__:
    sys.exit(main(sys.argv))
