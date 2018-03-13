from change_license import change_license_for_jinja_content, change_license_for_js_content, change_license_for_html_content, change_license_for_rst_content, change_license_for_python_content
from textwrap import dedent
import datetime


def test_license_text_changers(example_contents):
    """Test license changers."""
    fns = {
        'jinja': change_license_for_jinja_content,
        'js': change_license_for_js_content,
        'html': change_license_for_html_content,
        'rst': change_license_for_rst_content,
        'python': change_license_for_python_content,
    }

    #example_contents = [example_contents[7], ]
    for idx, (filetype, in_text, exp_text) in enumerate(example_contents):
        out_text = fns[filetype](in_text)
        assert out_text == exp_text, "Failed at Idx: {0}".format(str(idx))
