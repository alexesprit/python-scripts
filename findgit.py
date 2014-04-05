# coding: utf-8

import os
import sys

import argparse


TYPE_LOCAL = 1 << 1
TYPE_REMOTE = 1 << 2


def get_repo_type(repo_directory):
    refs_path = os.path.join(repo_directory, '.git', 'refs')
    return TYPE_REMOTE if 'remotes' in os.listdir(refs_path) else TYPE_LOCAL


def find_git_repos(directory, search_mask):
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            repo_type = get_repo_type(root)
            if repo_type & search_mask:
                print u'Found git repo at %s' % os.path.abspath(root)
            dirs.remove('.git')
        # don't cd to dir if it's hidden
        for dir_ in dirs:
            if dir_.startswith('.'):
                dirs.remove(dir_)


def main():
    parser = argparse.ArgumentParser(description='Search git repositories.')
    parser.add_argument(dest='directory', metavar='DIR', help='Path to scanning')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('-l', '--local', action='store_true', help='Seach local repositories only')
    group.add_argument('-r', '--remote', action='store_true', help='Search remote repositories only')

    args = parser.parse_args()
    if args.local:
        search_mask = TYPE_LOCAL
    elif args.remote:
        search_mask = TYPE_REMOTE
    else:
        search_mask = TYPE_LOCAL | TYPE_REMOTE
    try:
        find_git_repos(args.directory, search_mask)
    except KeyboardInterrupt:
        print 'Cancelled'


if __name__ == '__main__':
    sys.exit(main())
