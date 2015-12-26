# coding: utf-8

import os
import sys

from argparse import ArgumentParser
from argparse import RawTextHelpFormatter


DESCRIPTION = '''Search git repositories.

legend:
  L - local
  = - remote (up-to-date)
  ^ - remote (outdated)
  ? - unknown
'''


TYPE_LOCAL = 1 << 1
TYPE_REMOTE = 1 << 2
TYPE_OUTDATED = 1 << 3


def get_git_path(repo_path, *args):
    return os.path.join(repo_path, '.git', *args)


def get_git_object(repo_path, *args):
    object_path = get_git_path(repo_path, *args)
    if os.path.exists(object_path):
        with open(object_path, 'r') as fp:
            return fp.read().strip()
    return None


def process_repo(repo_directory, search_mask):
    repo_type = get_repo_type(repo_directory)
    if repo_type & search_mask:
        repo_name = os.path.basename(repo_directory)
        repo_path = os.path.abspath(repo_directory)

        if repo_type & TYPE_LOCAL:
            status = 'L'
        elif repo_type & TYPE_OUTDATED:
            status = '^'
        elif repo_type & TYPE_REMOTE:
            status = '='
        else:
            status = '?'

        print('[{2}] {0} [{1}]'.format(repo_name, repo_path, status))


def get_repo_type(repo_path):
    head = get_git_object(repo_path, 'refs', 'heads', 'master')
    orig_head = get_git_object(repo_path, 'refs', 'remotes', 'origin', 'master')

    if not orig_head:
        return TYPE_LOCAL
    else:
        if head == orig_head:
            return TYPE_REMOTE
        else:
            return TYPE_REMOTE | TYPE_OUTDATED


def find_git_repos(root, search_mask):
    try:
        dirs = [x for x in os.listdir(root)
                  if os.path.isdir(os.path.join(root, x))]
    except WindowsError:
        return
    if '.git' in dirs:
        process_repo(root, search_mask)
    else:
        for d in dirs:
            find_git_repos(os.path.join(root, d), search_mask)


def main():
    parser = ArgumentParser(prog='findgit',
                            description=DESCRIPTION,
                            formatter_class=RawTextHelpFormatter)
    parser.add_argument(dest='directory', metavar='DIR', help='Path to scanning')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-l', '--local', action='store_true', help='Search local repositories only')
    group.add_argument('-r', '--remote', action='store_true', help='Search remote repositories only')
    group.add_argument('-o', '--outdated', action='store_true', help='Search outdated repositories only')

    args = parser.parse_args()
    if args.local:
        search_mask = TYPE_LOCAL
    elif args.remote:
        search_mask = TYPE_REMOTE
    elif args.outdated:
        search_mask = TYPE_OUTDATED
    else:
        search_mask = TYPE_LOCAL | TYPE_REMOTE
    try:
        find_git_repos(args.directory, search_mask)
    except KeyboardInterrupt:
        print('Cancelled')


if __name__ == '__main__':
    sys.exit(main())
