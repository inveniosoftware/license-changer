from change_license import change_license_for_jinja_content, change_license_for_js_content, change_license_for_html_content, change_license_for_rst_content
from textwrap import dedent
import datetime


def test_license_text_changers(example_contents):
    """Test license changers."""
    fns = {
        'jinja': change_license_for_jinja_content,
        'js': change_license_for_js_content,
        'html': change_license_for_html_content,
        'rst': change_license_for_rst_content,
    }

    for filetype, in_text, exp_text in example_contents:
        out_text = fns[filetype](in_text)
        assert out_text == exp_text
