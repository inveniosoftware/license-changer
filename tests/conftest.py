import pytest
import os

@pytest.fixture()
def example_contents():
    filenames = {
        'jinja': [
            ('jinja_1.html', 'jinja_1.out.html'),
            ('jinja_2.html', 'jinja_2.out.html'),
        ]
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

