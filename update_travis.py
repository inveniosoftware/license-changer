#!/usr/bin/env python3

"""
Update .travis.yml file:
* If there are builds with REQUIREMENTS=devel, it adds them to the list of
  builds that are allowed to fail.

Usage:
  $ ./update_travis.py /path/to/repo/.travis.yml
  $ git commit -a -s -m 'travis: update pypi password, add allow_failures'
"""

import click
import os


def add_allow_failures(filename):
    """Add allow_failures to .travis.yml file."""
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


def _get_pypi_password(repository):
    """Return the new pypi password for a given repository."""
    passwords_file = os.path.join(os.path.dirname(__file__),
                                  'pypi-password-travis.txt')
    with open(passwords_file) as f:
        pypi_passwords = f.readlines()
    for password in pypi_passwords:
        if 'inveniosoftware/{0}: '.format(repository) in password:
            return password.split(': ')[-1].rstrip('\n')


def update_pypi_passwords(filename):
    """Update pypi username and password."""
    old_file = open(filename, 'r')
    lines = old_file.readlines()
    old_file.close()

    new_file = open(filename, 'w')
    inside_deploy = False
    for line in lines:
        # Check if we are inside 'deploy:' section of .travis.yml
        if 'deploy:' in line:
            inside_deploy = True
        if inside_deploy:
            if line.startswith('  user: '):
                new_file.write('  user: inveniosoftware\n')
                continue
            elif line.startswith('    secure:'):
                travis_file_dir = os.path.dirname(os.path.realpath(filename))
                repository = travis_file_dir.split('/')[-1]
                new_pass = _get_pypi_password(repository)
                if not new_pass:
                    print("No password for {0} repository".format(repository))
                    print("Keeping the old password!")
                    new_file.write(line)
                    continue
                else:
                    new_file.write('    secure: "{0}"\n'.format(new_pass))
                    continue
        new_file.write(line)
    new_file.close()


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def main(filename):
    """Cleanup files."""
    filename_basename = os.path.basename(filename)
    if filename_basename == '.travis.yml':
        add_allow_failures(filename)
        update_pypi_passwords(filename)


if __name__ == '__main__':
    main()
