from change_license import functs
from textwrap import dedent
import datetime


def test_license_text_changers(example_contents):
    """Test license changers."""

    #example_contents = [example_contents[13], ]
    for idx, (filetype, in_text, exp_text) in enumerate(example_contents):
        out_text, touched = functs[filetype](in_text)
        assert out_text == exp_text, "Failed at Idx: {0}".format(str(idx))
