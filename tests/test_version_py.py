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

    assert change_version_py(text1) == expected1

    # Shouldn't be changed
    text = "__version__ = '1.0.0'"
    assert change_version_py(text) == text
    text = "__version__ = '0.1.0'"
    assert change_version_py(text) == text
    text = "__version__ = '0.3.5'"
    assert change_version_py(text) == text

    # Should be changed
    expected = "__version__ = '1.0.0'"  # note the single quotes ''
    text = "__version__ = '1.0.0a5.dev20170223'"
    assert change_version_py(text) == expected
    text = '__version__ = "1.0.0b1.dev20160000"'
    assert change_version_py(text) == expected
    text = '__version__ = "1.0.0.dev20170223"'
    assert change_version_py(text) == expected
    text = '__version__ = "1.0.0.a1"'
    assert change_version_py(text) == expected
    text = '__version__ = "1.0.0a1"'
    assert change_version_py(text) == expected
    text = '__version__ = "1.0.0"'
    assert change_version_py(text) == expected
