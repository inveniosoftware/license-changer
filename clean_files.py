#!/usr/bin/env python3

"""
Clean some files:
* Remove pytest-cache from setup.py file (as it's now part of pytest)

Usage:
  $ ./clean_files.py setup.py
  $ git commit -a -s -m 'global: cleanup of dependencies'
"""

import click
import os


def clean_setup_file(filename):
    """Clean the setup.py file."""
    old_file = open(filename, 'r')
    lines = old_file.readlines()
    old_file.close()

    new_file = open(filename, 'w')
    for line in lines:
        # pytest-cache is now part of pytest, so let's remove it
        if "'pytest-cache>=1.0" not in line:
            new_file.write(line)
    new_file.close()


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def main(filename):
    """Cleanup files."""
    filename_basename = os.path.basename(filename)
    if filename_basename == 'setup.py':
        clean_setup_file(filename)


if __name__ == '__main__':
    main()
