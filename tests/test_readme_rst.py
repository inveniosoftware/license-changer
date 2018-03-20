from utils import update_readme_rst
from textwrap import dedent

def test_pypy_classifier():
    text1 = dedent("""\
        ================
         Invenio-MARC21
        ================

        .. image:: https://img.shields.io/travis/inveniosoftware/invenio-marc21.svg
                :target: https://travis-ci.org/inveniosoftware/invenio-marc21

        .. image:: https://img.shields.io/coveralls/inveniosoftware/invenio-marc21.svg
                :target: https://coveralls.io/r/inveniosoftware/invenio-marc21

        .. image:: https://img.shields.io/github/tag/inveniosoftware/invenio-marc21.svg
                :target: https://github.com/inveniosoftware/invenio-marc21/releases

        .. image:: https://img.shields.io/pypi/dm/invenio-marc21.svg
                :target: https://pypi.python.org/pypi/invenio-marc21

        .. image:: https://img.shields.io/github/license/inveniosoftware/invenio-marc21.svg
                :target: https://github.com/inveniosoftware/invenio-marc21/blob/master/LICENSE


        Invenio module with nice defaults for MARC21 overlay.

        *This is an experimental developer preview release.*

        * Free software: MIT license
        * Documentation: https://invenio-marc21.readthedocs.io/""")

    exp_text1 = dedent("""\
        ================
         Invenio-MARC21
        ================

        .. image:: https://img.shields.io/travis/inveniosoftware/invenio-marc21.svg
                :target: https://travis-ci.org/inveniosoftware/invenio-marc21

        .. image:: https://img.shields.io/coveralls/inveniosoftware/invenio-marc21.svg
                :target: https://coveralls.io/r/inveniosoftware/invenio-marc21

        .. image:: https://img.shields.io/pypi/v/invenio-marc21.svg
                :target: https://pypi.org/pypi/invenio-marc21


        Invenio module with nice defaults for MARC21 overlay.

        *This is an experimental developer preview release.*

        * Free software: MIT license
        * Documentation: https://invenio-marc21.readthedocs.io/""")

    assert update_readme_rst(text1) == exp_text1
