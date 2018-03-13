import pytest
import os

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture()
def example_contents():
    filenames = [
        #('jinja_1.html', 'jinja_1.out.html'),
        #('jinja_2.html', 'jinja_2.out.html'),
        #('js_1.js', 'js_1.out.js'),
        ('html_1.html', 'html_1.out.html'),
        #('rst_1.rst', 'rst_1.out.rst'),
        #('rst_2.rst', 'rst_2.out.rst'),
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

