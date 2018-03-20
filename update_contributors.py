#!/usr/bin/env python3

"""
Update AUTHORS.rst file:
* Regenerate the list of contributors, based on git log messages (completely
  replaces the previous content of the file).

Usage:
  $ ./update_contributors.py path/to/github/repository
  $ git commit -a -s -m 'authors: update the list of contributors'
"""

import os
import yaml
import subprocess

import click


with open('./contributors.yaml') as f:
    CONTRIBUTORS = yaml.load(f)

# List of authors that should not be added to the contributors file
SKIPPED_AUTHORS = ['',
                   'Invenio',
                   'Invenio-Developers']

# There are some special cases - e.g. when users are not putting their full
# name in the commit message, typos, etc.
SPECIAL_CASES = {
    'Alberto': 'Alberto Rodriguez Peon',
    'Diego': 'Diego Rodriguez',
    'giannistsan': 'Ioannis Tsanaktsidis',
    'Nicola': 'Nicola Tarocco',
    'Paulina': 'Paulina Lach',
    'Paulina1': 'Paulina Lach',
    'valkyrie': 'Valkyrie Savage',
}

# Name of the file for storing the list of contributors
CONTRIBUTORS_FILE = 'AUTHORS.rst'

LICENSE = """\
..
    This file is part of Invenio.
    Copyright (C) 2016-2018 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

"""


def _get_name(author):
    """Get full name of an author.

    If `author` is a github username, it tries to get the real name from
    contributors.yaml file.
    """
    if len(author.split()) >= 2 and author[0].isupper():
        # It's probably a full name already
        return author
    if author not in CONTRIBUTORS.keys():
        print("GitHub user: {0} not in contributors.yaml!".format(author))
    if not CONTRIBUTORS.get(author):
        print("Unknown full name for GitHub user: {0}".format(author))
    return CONTRIBUTORS.get(author)


def update_contributors(repository):
    """Regenerate the content of AUTHORS.rst."""

    task = subprocess.Popen('git -C {0} log --pretty=format:"%aN" |'
                            ' sort | uniq'.format(repository),
                            shell=True,
                            stdout=subprocess.PIPE)
    data = task.stdout.read()
    authors_list = data.decode('utf-8').split('\n')

    # We want to keep the alphabetical order and names resolved from github
    # usernames won't be in the alphabetical order, so we first create the
    # list of unique authors, then we sort it and put into a file
    unique_authors = []
    for author in authors_list:
        if author in SKIPPED_AUTHORS:
            continue
        if author in SPECIAL_CASES.keys():
            author_name = SPECIAL_CASES[author]
        else:
            author_name = _get_name(author)
        # Avoid duplicating authors - maybe they used github username for some
        # commits and full name for others?
        if author_name and author_name not in unique_authors:
            unique_authors.append(author_name)

    authors_file = open(os.path.join(repository, CONTRIBUTORS_FILE), 'w')
    authors_file.write(LICENSE)
    authors_file.write("Contributors\n")
    authors_file.write("============\n")
    authors_file.write("\n")
    for author in sorted(unique_authors):
        authors_file.write("- {0}\n".format(author))
    authors_file.close()


@click.command()
@click.argument('repository', type=click.Path(exists=True))
def main(repository):
    update_contributors(repository)


if __name__ == '__main__':
    main()
