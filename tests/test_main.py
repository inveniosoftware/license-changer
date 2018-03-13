# content of tests.py

from change_license import raw_update_copyright_years, \
    YEARS_RE_PATTERN_PYTHON, YEARS_RE_PATTERN_JS, very_good_solushen
from textwrap import dedent
import re


def test_years_re_match_python():
    # 2015-2018

    text1 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2003, 2004, 2005 CERN."
    foobar = 123
    def main():
        pass
    """)

    # 2015-2018
    text2 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
    #               2011, 2012, 2013 CERN."
    foobar = 123
    def main():
        pass
    """)

    # 2016-201
    text3 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2016 CERN."
    foobar = 123
    def main():
        pass
    """)

    # 2018
    text4 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2018 CERN."
    foobar = 123
    def main():
        pass
    """)

    expected1 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2015-2018 CERN."
    foobar = 123
    def main():
        pass
    """)

    expected2 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2016-2018 CERN."
    foobar = 123
    def main():
        pass
    """)

    expected3 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2018 CERN."
    foobar = 123
    def main():
        pass
    """)

    # TODO: come up with good pattern here
    pat = r'(.*Copyright \(C\) )(?P<first_year>[0-9]*).* CERN\.'

    assert very_good_solushen(text1, pat) == expected1

    # assert raw_update_copyright_years(text2, pat) == expected1
    # assert raw_update_copyright_years(text3, pat) == expected2
    # assert raw_update_copyright_years(text4, pat) == expected3
