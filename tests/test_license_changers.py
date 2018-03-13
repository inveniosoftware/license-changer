from change_license import change_license_for_jinja_content
from textwrap import dedent
import datetime


def test_jinja_text(example_contents):
    """Test jinja files license changer."""

    for filetype, examples in example_contents.items():
        for in_text, exp_text in examples:
            out_text = change_license_for_jinja_content(in_text, '2015-2018')
            assert out_text == exp_text
