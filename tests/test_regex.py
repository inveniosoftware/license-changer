import sys
sys.path.append('..')
from change_license import get_first_year_from_file, \
    YEARS_RE_PATTERN_PYTHON, YEARS_RE_PATTERN_JS
from textwrap import dedent
import re


def test_years_re_match_python():
    # 2003
    text1 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2003, 2004, 2005 CERN.
    foobar = 123
    def main():
        pass
    """)

    # 2003
    text2 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
    #               2011, 2012, 2013 CERN.
    foobar = 123
    def main():
        pass
    """)

    # 2016
    text3 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2016 CERN.
    foobar = 123
    def main():
        pass
    """)

    # 2016
    text4 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) 2018 CERN.
    foobar = 123
    def main():
        pass
    """)

    # 2018
    text5 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C)     2018   ,   2004, 2005, 2006, 2007, 2008,
    #               2011, 2012, 2013 CERN.
    foobar = 123
    def main():
        pass
    """)

    expected1 = '2003'
    expected2 = '2003'
    expected3 = '2016'
    expected4 = '2018'
    expected5 = '2018'

    assert get_first_year_from_file(text1) == expected1
    assert get_first_year_from_file(text2) == expected2
    assert get_first_year_from_file(text3) == expected3
    assert get_first_year_from_file(text4) == expected4
    assert get_first_year_from_file(text5) == expected5
