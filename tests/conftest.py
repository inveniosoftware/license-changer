import pytest
import os

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture()
def example_contents():
    filenames = {
        'jinja': [
            ('jinja_1.html', 'jinja_1.out.html'),
            ('jinja_2.html', 'jinja_2.out.html'),
        ],
        'js': [
            ('js_1.js', 'js_1.out.js'),
        ],
        'html': [
            ('html_1.html', 'html_1.out.html'),
        ],
        'rst': [
            ('rst_1.rst', 'rst_1.out.rst'),
            ('rst_2.rst', 'rst_2.out.rst'),
        ],
    }
    contents = dict((k, []) for k in filenames.keys())
    # Load all files contents
    dpath = os.path.join(os.path.dirname(__file__), 'data')
    for k, v in filenames.items():
        for in_fn, out_fn in v:
            with open(os.path.join(dpath, in_fn), 'r') as fp:
                in_cnt = fp.read()
            with open(os.path.join(dpath, out_fn), 'r') as fp:
                out_cnt = fp.read()
            contents[k].append((in_cnt, out_cnt))
    return contents

