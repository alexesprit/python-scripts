# coding: utf-8

import os
import sys


def find_git_repos(folder):
    child_folders = os.listdir(folder)
    if '.git' in child_folders:
        print u'Found git repo at %s' % folder
    else:
        for child_item in child_folders:
            child_item_path = os.path.join(folder, child_item)
            if os.path.isdir(child_item_path):
                find_git_repos(child_item_path)


def main(args):
    search_folder = args[1]
    find_git_repos(search_folder)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
