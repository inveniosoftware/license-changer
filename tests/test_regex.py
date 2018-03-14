import sys
sys.path.append('..')
from change_license import get_first_year_from_file
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
    # Copyright (C)2016CERN.
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

    # None
    text6 = dedent("""# -*- coding: utf-8 -*-
    # This file is part of Invenio.
    # Copyright (C) CERN.
    foobar = 123
    def main():
        pass
    """)

    assert get_first_year_from_file(text1) == '2003'
    assert get_first_year_from_file(text2) == '2003'
    assert get_first_year_from_file(text3) == '2016'
    assert get_first_year_from_file(text4) == '2016'
    assert get_first_year_from_file(text5) == '2018'
    assert get_first_year_from_file(text6) == None
