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


OLD_LICENSE_SUBSTR = 'modify it under the terms of the GNU'
NEW_LICENSE_SUBSTR = 'under the terms of the MIT License'

LICENSE_NEW_CODE = 'MIT'

LICENSE_NEW_TROVE = 'License :: OSI Approved :: MIT License'

PROJECT_NAME = 'Invenio'
LICENSE_NEW_FULLHEADER_JINJA = """{{# -*- coding: utf-8 -*-

  This file is part of {name}.
  Copyright (C) {years} CERN.

  {name} is free software; you can redistribute it and/or modify it
  under the terms of the MIT License; see LICENSE file for more details.
#}}"""
LICENSE_NEW_FULLHEADER_JS = """/*
 * This file is part of {name}.
 * Copyright (C) {years} CERN.
 *
 * {name} is free software; you can redistribute it and/or modify it
 * under the terms of the MIT License; see LICENSE file for more details.
 */"""

LICENSE_NEW_FULLHEADER_RST = """..
    This file is part of Invenio.
    Copyright (C) {years} CERN.

    {name} is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.
"""

LICENSE_NEW_FULLHEADER_HTML = """<!--
  This file is part of {name}.
  Copyright (C) {years} CERN.

  {name} is free software; you can redistribute it and/or modify it
  under the terms of the MIT License; see LICENSE file for more details.
-->"""

LICENSE_NEW_FULLHEADER_PYTHON = """# -*- coding: utf-8 -*-
#
# This file is part of {name}.
# Copyright (C) {years} CERN.
#
# {name} is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details."""

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

FIRST_YEAR_RE_PATTERN = r'^.*(Copyright \(C\) *)(?P<first_year>[0-9]+).*'


def get_commit_years(filename):
    """Return commit years for filename.

    Use '.' for the whole git repository.
    """
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
    years = fmt.format(start=lo, end=hi) if lo < hi else str(max(lo, hi))
    return years

def get_years_string_from_file(filename, **kwargs):
    """Return a copyright years string for the file (looks at commit dates).

    returns: Copyright years string, e.g.: '2015-2018' or '2018'.
    """
    min_year = min(get_commit_years(filename))  # min(['2013', '2014', ... ])
    return get_years_string(min_year, **kwargs)


def change_license_for_LICENSE_file(filename):
    """Change license for LICENSE file. Special treatment."""
    fdesc = open(filename, 'w')
    fdesc.write(LICENSE_NEW_HEADER)
    fdesc.write('\n')
    fdesc.write('Copyright (C) ' + get_years_string_from_file(filename) + ' CERN.')
    fdesc.write('\n\n')
    fdesc.write(LICENSE_NEW_BODY)
    fdesc.close()


def change_license_for_docslicenserst_file(filename):
    """Change license for docs/license.rst file. Special treatment."""
    fdesc = open(filename, 'w')
    fdesc.write('License\n')
    fdesc.write('=======\n\n')
    fdesc.write('.. include:: ../LICENSE')
    fdesc.write('\n')
    fdesc.close()


def do_not_change_license(filename):
    "Do not change license. Useful for PO files, graphics, etc."
    print('[INFO] Ignoring file', filename)


def find_prefix_suffix(text, start, end, inside):
    """Find the prefix and suffix separated by comment block."""
    s = text.find(start)
    if s == -1:
        return None
    e = text.find(end, s + len(start))
    i = text.find(inside, s + len(start))
    while e > 0 and (i == -1 or i > e):
        s = text.find(start, e + len(end))
        if s != -1:
            e = text.find(end, s + len(start))
            i = text.find(inside, s + len(start))
        else:
            return None
    if i >= 0 and i < e:
        return text[:s], text[e + len(end):]


def del_license_for_rst_content(text, years=None, add_missing=False):
    """Remove the license header from RST files."""
    # detect license block end:
    license_block_end = 'submit itself to any jurisdiction.'
    if license_block_end in text:
        pass  # good, we found it
    else:
        license_block_end = 'MA 02111-1307, USA.'
        if license_block_end in text:
            pass  # good, we found it
        else:
            return text, False  # License not found, return original text
    # update the file until license block end:
    license_block_p = True
    main_content_p = False
    new_output = []
    for line in text.split('\n'):
        line = line.rstrip()
        if license_block_p:
            if license_block_end in line:
                license_block_p = False
        else:
            if main_content_p:
                new_output.append(line)
            else:
                if len(line):
                    main_content_p = True
                    new_output.append(line)
                else:
                    # ignore empty lines immediately after copyright
                    pass
    # TODO: We don't always modify, second parameter can be False
    return '\n'.join(new_output), True


def change_license_in_block_comment(text, years='2015-2018', start_str='/*',
        end_str='*/', formatter=LICENSE_NEW_FULLHEADER_JS, add_missing=True):
    """Generic license swapper for block-commend headers."""
    # Try to fetch the first copyright year from an existing header file
    # If it's not there, fall-back to the default
    year = get_first_year_from_file(text)
    years = get_years_string(year) if year else years

    # If new license is found, skip
    if NEW_LICENSE_SUBSTR in text:
        return text, False

    # Try to find old license
    pref_suff = find_prefix_suffix(text, start_str, end_str, OLD_LICENSE_SUBSTR)
    # If the block split wasn't found, concatenate with full text
    if not pref_suff:
        prefix, suffix = '', '\n' + text
    else:
        prefix, suffix = pref_suff

    if pref_suff or add_missing:
        license_text = formatter.format(years=years, name=PROJECT_NAME)
        out = prefix + license_text + suffix
        return out, True
    else:
        return text, False


def change_license_for_jinja_content(text, years='2015-2018', add_missing=True):
    text, touched = change_license_in_block_comment(text, years=years,
        start_str='{#', end_str='#}', formatter=LICENSE_NEW_FULLHEADER_JINJA,
        add_missing=add_missing)
    return text, touched


def change_license_for_js_content(text, years='2015-2018', add_missing=True):
    if NEW_LICENSE_SUBSTR in text:
        return text, False
    s_str = '// This file is part of '
    e_str = 'submit itself to any jurisdiction.'
    if find_prefix_suffix(text, s_str, e_str, OLD_LICENSE_SUBSTR):
        text, touched = change_license_in_block_comment(text, years=years,
            start_str=s_str, end_str=e_str, formatter=LICENSE_NEW_FULLHEADER_JS,
            add_missing=add_missing)
    else:
        text, touched = change_license_in_block_comment(text, years=years,
            start_str='/*', end_str='*/', formatter=LICENSE_NEW_FULLHEADER_JS,
            add_missing=add_missing)
    return text, touched


def change_license_for_scss_content(text, years='2015-2018', add_missing=True):
    text, touched = change_license_in_block_comment(text, years=years,
        start_str='//', end_str='//', formatter=LICENSE_NEW_FULLHEADER_JS,
        add_missing=add_missing)
    return text, touched


def change_license_for_html_content(text, years='2015-2018', add_missing=True):
    text, touched = change_license_in_block_comment(text, years=years,
        start_str='<!--', end_str='-->', formatter=LICENSE_NEW_FULLHEADER_HTML,
        add_missing=add_missing)
    return text, touched


def change_license_for_rst_content(text, years='2015-2018', add_missing=True):
    s_str = '..\n    This file is part of'
    e_str = 'submit itself to any jurisdiction.'
    text, touched = change_license_in_block_comment(text, years=years,
        start_str=s_str, end_str=e_str, formatter=LICENSE_NEW_FULLHEADER_RST,
        add_missing=add_missing)
    return text, touched


def change_license_for_python_content(text, years='2015-2018', add_missing=True):
    # First try to match block starting with utf-8 coding tag
    s_str1 = '# -*- coding: utf-8 -*-'  # Encoding start
    s_str2 = '# This file is part of '  # License start

    e_str1 = '111-1307, USA.'  # GPL part
    e_str2 = 'submit itself to any jurisdiction.'  # CERN part

    touched = False

    # Remove leading comment blocks
    i = 0
    text_sp = text.split('\n')
    while re.match(r'^\s*#\s*$', text_sp[i]):
        i += 1
        touched = True
    text = '\n'.join(text_sp[i:])

    if NEW_LICENSE_SUBSTR in text:
        return text, touched
    # Try to match possible license blocks starting from the "widest",
    # i.e.: the ones encapsulating the most text
    for s_str, e_str in [(s_str1, e_str2), (s_str1, e_str1),
                         (s_str2, e_str2), (s_str2, e_str1)]:
        if find_prefix_suffix(text, s_str, e_str, OLD_LICENSE_SUBSTR):
            text, touched = change_license_in_block_comment(text, years=years,
                start_str=s_str, end_str=e_str, add_missing=add_missing,
                formatter=LICENSE_NEW_FULLHEADER_PYTHON)
            break
    if not touched and add_missing:
        text, touched = change_license_in_block_comment(text, years=years,
            start_str=s_str1, end_str=e_str2, add_missing=add_missing,
            formatter=LICENSE_NEW_FULLHEADER_PYTHON)
    return text, touched


def change_license_for_any_content(text, years='2015-2018'):
    """Try to match the license by any matcher."""
    fns = [
        change_license_for_jinja_content,
        change_license_for_js_content,
        change_license_for_html_content,
        change_license_for_python_content,
    ]
    touched = False
    for fn in fns:
        text, touched = fn(text, years=years, add_missing=False)
        if touched:
            break
    return text, touched


def change_license_for_source_file(filename, change_function):
    """Change the license for a source file (js, html, scss, py)."""
    with open(filename, 'r') as fp:
        content = fp.read()
    years = get_years_string_from_file(filename)
    out, touched = change_function(content, years=years)
    if touched:
        with open(filename, 'w') as fp:
            fp.write(out)
        return True
    return False


def get_first_year_from_file(content, pattern=FIRST_YEAR_RE_PATTERN):
    "Update copyright year list for filename if the current year is not listed."
    first_year = None
    for line in content.split('\n'):
        match = re.search(pattern, line)
        if match:
            first_year = match.group('first_year')
    return first_year


def setup_py_update_trove_classifiers(filename):
    "Update Trove classifiers in setup.py filename."
    old_content = open(filename, 'r').read()
    new_content = re.sub(r"license='.*',", "license='" + LICENSE_NEW_CODE + "',", old_content)
    new_content = re.sub(r"'License :: OSI Approved ::.*'", "'" + LICENSE_NEW_TROVE + "'", new_content)
    fdesc = open(filename, 'w')
    fdesc.write(new_content)
    fdesc.close()


def change_GPLv2_to_MIT(filename):
    """Change license for LICENSE file. Special treatment."""
    old_content = open(filename, 'r').read()
    new_content = re.sub(r'GPLv2', 'MIT', old_content)
    if old_content != new_content:
        fdesc = open(filename, 'w')
        fdesc.write(new_content)
        fdesc.close()
        return True
    return False



# Mapping from filetype to text changer function
FILETYPE2FN = {
    'jinja': change_license_for_jinja_content,
    'js': change_license_for_js_content,
    'html': change_license_for_html_content,
    'rst': change_license_for_rst_content,
    'python': change_license_for_python_content,
    'all': change_license_for_any_content,
}

# Mapping from filename to text changer function
FILENAME2FN = {
    '.editorconfig': change_license_for_python_content,
    '.travis.yml': change_license_for_python_content,
    'MANIFEST.in': change_license_for_python_content,
    'babel.ini': change_license_for_python_content,
    'pytest.ini': change_license_for_python_content,
    'requirements-devel.txt': change_license_for_python_content,
    'run-tests.sh': change_license_for_python_content,
    'setup.cfg': change_license_for_python_content,
    'config': change_license_for_python_content,
}

@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.argument('projectname', type=str, default='Invenio')
def main(filename, projectname):
    "Change license of the filename."
    global PROJECT_NAME
    PROJECT_NAME = projectname

    filename_basename = os.path.basename(filename)
    if filename_basename == 'LICENSE':
        change_license_for_LICENSE_file(filename)
    elif filename_basename == 'license.rst':
        change_license_for_docslicenserst_file(filename)
    else:
        path_prefix, extension = os.path.splitext(filename)
        fn = None
        if extension in ('.xsl',):
            print('[INFO] Purposedly skipped file', filename)
            return
        if filename_basename in FILENAME2FN:
            fn = FILENAME2FN[filename_basename]
        elif extension in ('.rst', ):
            fn = FILETYPE2FN['rst']
        elif extension in ('.py', ):
            fn = FILETYPE2FN['python']
        elif extension in ('.js', '.scss', ):
            fn = FILETYPE2FN['js']
        elif extension in ('.html', ) and ('src' in path_prefix or 'static' in path_prefix):
            fn = FILETYPE2FN['html']
        elif extension in ('.html', ) and ('src' not in path_prefix) and ('static' not in path_prefix) and 'templates' in path_prefix:
            fn = FILETYPE2FN['jinja']
        else:
            fn = FILETYPE2FN['all']

        changed = change_license_for_source_file(filename, fn)
        if changed:
            print('[INFO] Changed file', filename)
        else:
            print('[INFO] Ignored file', filename)

        # Post-processors
        if filename_basename == 'setup.py':
            setup_py_update_trove_classifiers(filename)
            print('[INFO] Updated Trove', filename)
        changed = change_GPLv2_to_MIT(filename)
        if  changed:
            print('[INFO] Found and updated GPLv2 -> MIT', filename)


if __name__ == '__main__':
    main()
