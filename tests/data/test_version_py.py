from textwrap import dedent
import re

from utils import change_version_py


def test_change_version_py():
    text1 = dedent("""\
        # -*- coding: utf-8 -*-
        #
        # This file is part of Invenio.
        # Copyright (C) 2015-2018 CERN.
        #
        # Invenio is free software; you can redistribute it and/or modify it
        # under the terms of the MIT License; see LICENSE file for more details.

        from __future__ import absolute_import, print_function

        __version__ = '1.0.0b7'""")

    expected1 = dedent("""\
        # -*- coding: utf-8 -*-
        #
        # This file is part of Invenio.
        # Copyright (C) 2015-2018 CERN.
        #
        # Invenio is free software; you can redistribute it and/or modify it
        # under the terms of the MIT License; see LICENSE file for more details.

        from __future__ import absolute_import, print_function

        __version__ = '1.0.0'""")
    lol = change_version_py(text1)

    assert change_version_py(text1) == expected1
