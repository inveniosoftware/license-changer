#!/usr/bin/env python3

"""
Change license headers of a source code file.

Usage:
  $ cd private/src/invenio-oaiserver
  $ git checkout -b license-change
  $ for file in $(git ls-files); do change_license $file; done
  $ git commit -a -s -m 'global: license change to MIT License'
  $ git grep 'distributed in the hope that'
"""

import click
import datetime
import fileinput
import os
import re
import subprocess
from collections import defaultdict


LICENSE_OLD_START = {
    'python': '# Invenio is free software; you can redistribute it',
    'rst': """..
    This file is part of Invenio.""",
    'js': ' * Invenio is free software; you can redistribute',
    'html': '<!-- Copyright (C) '
}

LICENSE_NEW_CODE = 'MIT'

LICENSE_NEW_TROVE = 'License :: OSI Approved :: MIT License'

LICENSE_NEW_INFILE = """\
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details."""

LICENSE_NEW_FULLHEADER_JINJA = """-*- coding: utf-8 -*-

  This file is part of Invenio.
  Copyright (C) {years} CERN.

  Invenio is free software; you can redistribute it and/or modify it
  under the terms of the MIT License; see LICENSE file for more details."""

LICENSE_NEW_INFILE_JS = """\
 * Invenio is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details."""

LICENSE_NEW_HEADER = """\
MIT License
"""

LICENSE_NEW_BODY = """\
Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

In applying this license, CERN does not waive the privileges and immunities
granted to it by virtue of its status as an Intergovernmental Organization or
submit itself to any jurisdiction.
"""

YEARS_RE_PATTERN_PYTHON = r'^(.*# Copyright \(C\).* )([0-9]+) (CERN.*)$'
YEARS_RE_PATTERN_JS = r'^(.* \* Copyright \(C\).* )([0-9]+) (CERN.*)$'


def get_commit_years(filename):
    """Return commit years for filename.

    Use '.' for the whole git repository."""
    years = {}
    out = subprocess.getoutput('git log --follow --date=short --pretty=format:"%cd" -- ' + filename)
    if out:
        for line in out.split('\n'):
            years[line[0:4]] = 1
    years = list(years.keys())
    years.sort()
    return years

def get_years_string(year, fmt='{start}-{end}', lower_year='2015',
        upper_year=None):
    """Return a copyright years string for the minimum year from old license.

    The output is a range: '2013-2018' or a single year '2018'. We also impose
    a minimum year where the copyright holds (e.g.: '2015') as well as default
    maximum year, which is current year (at the time of the modification).

    param year: First contribution year, e.g.: '2013'
    type year: str
    returns: Copyright years string, e.g.: '2015-2018' or '2018'.
    """
    upper_year = upper_year or str(datetime.date.today().year)
    lo, hi = max(year, lower_year), upper_year
    # Return range ('2015-2018') if applicable, otherwise one year ('2018')
    years = fmt.format(start=lo, end=hi) if lo != hi else str(hi)
    return years

def get_years_string_from_file(filename, **kwargs):
    """Return a copyright years string for the file (looks at commit dates).

    returns: Copyright years string, e.g.: '2015-2018' or '2018'.
    """
    min_year = min(get_commit_years(filename))  # min(['2013', '2014', ... ])
    return get_years_string(min_year, **kwargs)


def change_license_for_LICENSE_file(filename):
    "Change license for LICENSE file. Special treatment."
    fdesc = open(filename, 'w')
    fdesc.write(LICENSE_NEW_HEADER)
    fdesc.write('\n')
    fdesc.write('Copyright (C) ' + ', '.join(get_commit_years('.')) + ' CERN.')
    fdesc.write('\n\n')
    fdesc.write(LICENSE_NEW_BODY)
    fdesc.close()


def change_license_for_docslicenserst_file(filename):
    "Change license for docs/license.rst file. Special treatment."
    fdesc = open(filename, 'w')
    fdesc.write('License\n')
    fdesc.write('=======\n\n')
    fdesc.write('.. include:: ../LICENSE')
    fdesc.write('\n')
    fdesc.close()


def do_not_change_license(filename):
    "Do not change license. Useful for PO files, graphics, etc."
    print('[INFO] Ignoring file', filename)


def change_license_for_rst_file(filename):
    "Change license for *.rst files."
    old_content = open(filename, 'r').read()
    # detect license block end:
    license_block_end = 'submit itself to any jurisdiction.'
    if license_block_end in old_content:
        pass  # good, we found it
    else:
        license_block_end = 'MA 02111-1307, USA.'
        if license_block_end in old_content:
            pass  # good, we found it
        else:
            license_block_end = 'XXXXXXXXXXXXXXXXXXXXXXXX'
    # update the file until license block end:
    license_block_p = True
    main_content_p = False
    print('[INFO] Changing file', filename)
    for line in fileinput.input(filename, inplace=True):
        line = line.rstrip()
        if license_block_p:
            if license_block_end in line:
                license_block_p = False
        else:
            if main_content_p:
                print(line)
            else:
                if len(line):
                    main_content_p = True
                    print(line)
                else:
                    # ignore empty lines immediately after copyright
                    pass

def change_license_for_jinja_content(text, years):
    if text.startswith('{#'):
        end = text.find('#}')
        body = text[end+3:]
    else:
        body = text

    out = '{# ' + LICENSE_NEW_FULLHEADER_JINJA.format(date=years) + '\n#}\n'
    out += body
    return out


def change_license_for_jinja_file(filename, years):
    "Add license header for *.html files that are jinja templates."
    print('[INFO] Changing file', filename)

    with open(filename, 'r') as fp:
        content = fp.read()
    years = get_years_string_from_file(filename)
    out = change_license_for_jinja_content(content, years)
    with open(filename, 'w') as fp:
        fp.write(out)
    return True


def change_license_for_js_file(filename):
    "Change license for *.js files. Return True if filename was touched."
    style = 'js'
    license_block_p = False
    filename_touched_p = False
    print('[INFO] Changing file', filename)
    for line in fileinput.input(filename, inplace=True):
        line = line.rstrip()
        if not license_block_p:
            if LICENSE_OLD_START[style] in line:
                license_block_p = True
            else:
                print(line)
        else:
            if line.startswith(' *') and not line.startswith(' */'):
                pass
            else:
                license_block_p = False
                print(LICENSE_NEW_INFILE_JS)
                print(line)
                filename_touched_p = True
    return filename_touched_p


def change_license_for_python_file(filename):
    "Change license for *.py files. Return True if filename was touched."
    style = 'python'
    license_block_p = False
    filename_touched_p = False
    print('[INFO] Changing file', filename)
    for line in fileinput.input(filename, inplace=True):
        line = line.rstrip()
        if not license_block_p:
            if LICENSE_OLD_START[style] in line:
                license_block_p = True
            else:
                print(line)
        else:
            if line.startswith('#'):
                pass
            else:
                license_block_p = False
                print(LICENSE_NEW_INFILE)
                print(line)
                filename_touched_p = True
    return filename_touched_p


def raw_update_copyright_years(content, pattern=YEARS_RE_PATTERN_PYTHON):
    "Update copyright year list for filename if the current year is not listed."
    current_year = str(datetime.date.today().year)
    newcontent = []
    for line in content.split('\n'):
        line = line.rstrip()
        match = re.match(pattern, line)
        if match:
            leader, year, trailer = match.groups()
            if year != current_year:
                newcontent.append(leader + year + ', ' + current_year + ' ' + trailer)
            else:
                newcontent.append(line)
        else:
            newcontent.append(line)
    return '\n'.join(newcontent)


def very_good_solushen(content, pattern=YEARS_RE_PATTERN_PYTHON):
    "Update copyright year list for filename if the current year is not listed."
    current_year = str(datetime.date.today().year)
    newcontent = []
    for line in content.split('\n'):
        line = line.rstrip()
        match = re.match(pattern, line)
        if match:
            leader, year = match.groups()
            if year != current_year:
                newcontent.append(leader + 'Copyright (C) ' + ', ' + current_year + ' ' + trailer)
            else:
                newcontent.append(line)
        else:
            newcontent.append(line)
    return '\n'.join(newcontent)


def update_copyright_years(filename, pattern=YEARS_RE_PATTERN_PYTHON):
    "Update copyright year list for filename if the current year is not listed."
    current_year = str(datetime.date.today().year)
    for line in fileinput.input(filename, inplace=True):
        line = line.rstrip()
        match = re.match(pattern, line)
        if match:
            leader, year, trailer = match.groups()
            if year != current_year:
                print(leader + year + ', ' + current_year + ' ' + trailer)
            else:
                print(line)
        else:
            print(line)


def need_to_process(filename, style='python'):
    "Do we need to process given file?"
    need_to_process_p = True
    old_content = open(filename, 'r').read()
    if LICENSE_OLD_START[style] not in old_content:
        print('[INFO] Ignoring file', filename)
        need_to_process_p = False
    return need_to_process_p


def setup_py_update_trove_classifiers(filename):
    "Update Trove classifiers in setup.py filename."
    old_content = open(filename, 'r').read()
    new_content = re.sub(r"license='.*',", "license='" + LICENSE_NEW_CODE + "',", old_content)
    new_content = re.sub(r"'License :: OSI Approved ::.*'", "'" + LICENSE_NEW_TROVE + "'", new_content)
    fdesc = open(filename, 'w')
    fdesc.write(new_content)
    fdesc.close()


@click.command()
@click.argument('filename', type=click.Path(exists=True))
def main(filename):
    "Change license of the filename."

    filename_basename = os.path.basename(filename)
    if filename_basename == 'LICENSE':
        change_license_for_LICENSE_file(filename)
    elif filename_basename == 'license.rst':
        change_license_for_docslicenserst_file(filename)
    else:
        path_prefix, extension = os.path.splitext(filename)
        if extension in ('.po', '.png', '.svg', '.gif', '.jpeg'):
            do_not_change_license(filename)
        elif extension in ('.rst', ):
            if need_to_process(filename, 'rst'):
                change_license_for_rst_file(filename)
        elif extension in ('.js', '.scss', ):
            if need_to_process(filename, 'js'):
                if change_license_for_js_file(filename):
                    update_copyright_years(filename, pattern=YEARS_RE_PATTERN_JS)
        elif extension in ('.html', ) and ('src' in path_prefix or 'static' in path_prefix):
            # Add HTML-style comments
            if need_to_process(filename, 'html'):
                pass
        elif extension in ('.html', ) and ('src' not in path_prefix) and ('static' not in path_prefix) and 'templates' in path_prefix:
            # Add Jinja-style comments
            change_license_for_jinja_file(filename)
        else:
            # we assume Python-style by default
            if need_to_process(filename, 'python'):
                if change_license_for_python_file(filename):
                    update_copyright_years(filename)
                    if filename_basename == 'setup.py':
                        setup_py_update_trove_classifiers(filename)


if __name__ == '__main__':
    main()
