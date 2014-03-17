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
    child_dirs = os.listdir(directory)
    if '.git' in child_dirs:
        repo_type = get_repo_type(directory)
        if repo_type & search_mask:
            print u'Found git repo at %s' % directory
    else:
        for child_item in child_dirs:
            child_item_path = os.path.join(directory, child_item)
            if os.path.isdir(child_item_path):
                find_git_repos(child_item_path, search_mask)


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
    find_git_repos(args.directory, search_mask)


if __name__ == '__main__':
    sys.exit(main())
