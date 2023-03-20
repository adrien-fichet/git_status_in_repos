# -*- coding: utf-8 -*-
"""Git status in dirs"""

import sys
import os.path
import argparse
import subprocess
import colorama
from termcolor import cprint


def setup_argument_parser():
    """Build the program argument parser and return it"""
    parser = argparse.ArgumentParser(
        prog="Git Status in Dirs",
        description="Find git status of all repositories in a given directory")
    parser.add_argument("directory", help="The directory containing git repositories")
    return parser


def get_directory_from_args(parser) -> str:
    """Retrieve the directory in which to run the program from sys args"""
    args = parser.parse_args()
    directory = args.directory

    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a directory")
        sys.exit(1)

    return directory


def search_for_git_repos_in_dir(directory):
    """Search for directories containing a git index, recursively in 
        the given directory"""
    print(f"Searching for git repositories in {directory}...")

    git_repos = []
    for root, dirs, _ in os.walk(directory):
        if ".git" in dirs:
            git_repos.append(root)

    print(f"Found {len(git_repos)} git repositories.")
    return git_repos


def git_status_in_dir(repo):
    """Print the git status of the given repository"""
    cprint(f"➔ {repo}: ", attrs=("bold",), end="")
    status = subprocess.check_output("git status -s", cwd=repo, shell=True).decode()
    if status == "":
        cprint("[OK]", "green")
    else:
        status = status.rstrip()
        cprint("[MODIFIED]", "red")
        print(status)
    return status


def main():
    """Program entry point"""
    colorama.init()
    parser = setup_argument_parser()
    directory = get_directory_from_args(parser) 
    git_repos = search_for_git_repos_in_dir(directory)

    for repo in git_repos:
        git_status_in_dir(repo)
