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

from change_license import get_years_string_from_file


contributors = os.path.join(os.path.dirname(__file__), 'contributors.yaml')
with open(contributors) as f:
    CONTRIBUTORS = yaml.load(f)

# List of authors that should not be added to the contributors file
SKIPPED_AUTHORS = ['',
                   'Invenio',
                   'Invenio-Developers',
                   'Cody',  # Cody was a bot from QuantifiedCode
                   ]

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
    'Adrian Tudor Panescu': 'Adrian-Tudor Panescu',
    'Jaime García': 'Jaime Garcia Llopis',
    'Javier Martin': 'Javier Martin Montull',
}

# Name of the file for storing the list of contributors
CONTRIBUTORS_FILE = 'AUTHORS.rst'

LICENSE = """\
..
    This file is part of {name}.
    Copyright (C) {years} CERN.

    {name} is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

"""

BASE_COMMITS = {
    'invenio': 'c4c292f9b3c3aaf65ea20cb74e4f3ec8ae4adcd9',
    'invenio-access': '5b2818387c9f833438fa30f67d47f529ecaa0968',
    'invenio-accounts': 'f97176828348baeb32bf9556001112ba49bcf4b2',
    'invenio-base': 'd8e31ee5f0e808a9b4cf37d9a987636e53439f32',
    'invenio-celery': '23dd4cdcc9699ae1a550d024055afbfbe34195ef',
    'invenio-collections': '99d5df278e5d6981d2a0c19c3abf90c29dcd005d',
    'invenio-communities': 'c76f30d38c69cb593edd97fee4d5cd690bcd136c',
    'invenio-deposit': 'aa654f01f9a9bd5b6ec19ae53326f04c4b1b1740',
    'invenio-formatter': '0733556a2fb8d7c524464b64c4de8b0e2ad0a246',
    'invenio-oaiharvester': 'a4325a61bc71a4aa4691d673a4bf4449671966f0',
    'invenio-oauth2server': '094323a759b837272d4a77a7141e80012939782f',
    'invenio-oauthclient': '7adadb59eab1dde241d2f041088dc79c1e190a56',
    'invenio-pages': '5f46a3c7194c5ef27f26c04699aa37a6c797afb2',
    'invenio-pidstore': 'b44142197566ef2ab6ecbed6d75dafd1e14da41b',
    'invenio-previewer': 'ede10b7f6172f81dda3a9f6695217892897dda08',
    'invenio-records': 'a685b1d0e0d62798619f3e084605bf42281b1f1c',
    'invenio-search': '1cd5740aae6022ffb0a781c3d63dd3b26b83dc61',
    'invenio-sequencegenerator': '1b55943e1f5e8dbf992b9d44412b2a783c415068',
    'invenio-webhooks': '43e2f1e7670781d57f7d1cf9c03bdf91f9afe23b',
}


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


def update_contributors(repository, projectname):
    """Regenerate the content of AUTHORS.rst."""
    # Strip the path to repository and get just the name
    repository_name = repository.rstrip('/').split('/')[-1]
    if repository_name in BASE_COMMITS:
        start = BASE_COMMITS.get(repository_name)
        task = subprocess.Popen(
            'git -C {0} log {1}^..HEAD --pretty=format:"%aN" |'
            ' sort | uniq'.format(repository, start),
            shell=True,
            stdout=subprocess.PIPE
        )
    else:
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

    authors_file_path = os.path.join(repository, CONTRIBUTORS_FILE)
    authors_file = open(authors_file_path, 'w')
    years = get_years_string_from_file(authors_file_path)
    authors_file.write(LICENSE.format(name=projectname, years=years))
    authors_file.write("Contributors\n")
    authors_file.write("============\n")
    authors_file.write("\n")
    for author in sorted(unique_authors):
        authors_file.write("- {0}\n".format(author))
    authors_file.close()


@click.command()
@click.argument('repository', type=click.Path(exists=True))
@click.argument('projectname', type=str, default='Invenio')
def main(repository, projectname):
    update_contributors(repository, projectname)


if __name__ == '__main__':
    main()
