import pytest
import os

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture()
def example_contents():
    filenames = [
        ('jinja_1.html', 'jinja_1.out.html'),

        # Ignore already parsed
        ('jinja_1.out.html', 'jinja_1.out.html'),
        ('jinja_2.html', 'jinja_2.out.html'),

        # Ignore already parsed
        ('jinja_2.out.html', 'jinja_2.out.html'),

        # jinja_3 has no header, add it
        ('jinja_3.html', 'jinja_3.out.html'),
        ('js_1.js', 'js_1.out.js'),

        # Ignore already parsed
        ('js_1.out.js', 'js_1.out.js'),

        # js_2 has top-level non-license header. Keep it and add license above.
        ('js_2.js', 'js_2.out.js'),

        # js_3 has no header, add it
        ('js_3.js', 'js_3.out.js'),
        ('html_1.html', 'html_1.out.html'),

        # Ignore already parsed
        ('html_1.out.html', 'html_1.out.html'),

        # html_2 has no header, should be added
        ('html_2.html', 'html_2.out.html'),
        ('rst_1.rst', 'rst_1.out.rst'),

        # Ignore already parsed
        ('rst_1.out.rst', 'rst_1.out.rst'),
        # TODO: Python not implemented
        ('python_1.py', 'python_1.out.py'),
        ('python_2.py', 'python_2.out.py'),
    ]
    # Load all files contents
    contents = []
    dpath = os.path.join(os.path.dirname(__file__), 'data')
    for in_fn, out_fn in filenames:
        filetype = in_fn.split('_')[0]
        with open(os.path.join(dpath, in_fn), 'r') as fp:
            in_cnt = fp.read()
        with open(os.path.join(dpath, out_fn), 'r') as fp:
            out_cnt = fp.read()
        contents.append((filetype, in_cnt, out_cnt))
    return contents

