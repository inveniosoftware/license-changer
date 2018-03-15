#!/usr/bin/env python3

"""
Update .travis.yml file:
* If there are builds with REQUIREMENTS=devel, it adds them to the list of
  builds that are allowed to fail.

Usage:
  $ ./update_travis.py .travis.yml
  $ git commit -a -s -m 'global: add allow_failures to travis config'
"""

import click
import os


def update_travis_config(filename):
    """Clean the setup.py file."""
    travis_file = open(filename, 'r')
    travis_config = travis_file.read()
    travis_file.close()
    if 'allow_failures' in travis_config:
        # allow_failures is already present in .travis.yml, we don't want to
        # overwrite it, it should be checked manually instead
        print('[INFO] `allow_failures` already in .travis.yml! Check manually')
        return
    if "\nmatrix:\n  fast_finish: true\n" not in travis_config:
        # travis config part with `matrix` options is different than in the
        # cookie-cutter, so it should be checked manually
        print("[INFO]! Non-standard .travis.yml configuration! Check manually")
        return

    old_travis = open(filename, 'r')
    lines = old_travis.readlines()
    old_travis.close()
    devel_build = []
    # On the first run through travis config, we gather all the lines that
    # contain the `devel` build settings
    for line in lines:
        if ' - REQUIREMENTS=devel' in line:
            devel_build.append(line.strip()[2:])
    if not devel_build:
        # No `devel` builds? So we don't change anything
        return
    # On the second run, we put the new configuration lines in the correct
    # place in .travis.yml
    old_file = open(filename, 'r')
    lines = old_file.readlines()
    old_file.close()

    new_file = open(filename, 'w')
    for line in lines:
        new_file.write(line)
        if line == "  fast_finish: true\n":
            new_file.write("  allow_failures:\n")
            for build in devel_build:
                new_file.write("    - env: {0}\n".format(build))
    new_file.close()


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def main(filename):
    """Cleanup files."""
    filename_basename = os.path.basename(filename)
    if filename_basename == '.travis.yml':
        update_travis_config(filename)


if __name__ == '__main__':
    main()
