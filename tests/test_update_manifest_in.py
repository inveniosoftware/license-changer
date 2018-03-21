from textwrap import dedent
import re

from utils import update_manifest_in


def test_update_manifest_in():
    text1 = dedent("""\
        # -*- coding: utf-8 -*-
        #
        # This file is part of Requirements-Builder
        # Copyright (C) 2015, 2016 CERN.
        #
        # Requirements-Builder is free software; you can redistribute it and/or
        # modify it under the terms of the Revised BSD License; see LICENSE
        # file for more details.

        include .coveragerc
        include .editorconfig
        include .isort.cfg
        include .lgtm MAINTAINERS
        include AUTHORS.rst
        include CHANGES.rst
        include CONTRIBUTING.rst
        include LICENSE
        include README.rst
        include RELEASE-NOTES.rst
        include docs/requirements.txt
        include pytest.ini
        include requirements.*.txt
        include run-tests.sh
        include tox.ini
        recursive-include docs *.rst conf.py Makefile
        recursive-include tests *
        recursive-exclude * *.py[co]
        recursive-exclude * __pycache__""")

    expected1 = dedent("""\
        # -*- coding: utf-8 -*-
        #
        # This file is part of Requirements-Builder
        # Copyright (C) 2015, 2016 CERN.
        #
        # Requirements-Builder is free software; you can redistribute it and/or
        # modify it under the terms of the Revised BSD License; see LICENSE
        # file for more details.

        include .coveragerc
        include .editorconfig
        include .isort.cfg
        include AUTHORS.rst
        include CHANGES.rst
        include CONTRIBUTING.rst
        include LICENSE
        include README.rst
        include docs/requirements.txt
        include pytest.ini
        include requirements.*.txt
        include run-tests.sh
        include tox.ini
        recursive-include docs *.rst conf.py Makefile
        recursive-include tests *
        recursive-exclude * *.py[co]
        recursive-exclude * __pycache__""")

    assert update_manifest_in(text1) == expected1

    text1 = dedent("""\
        include .lgtm MAINTAINERS RELEASE-NOTES.rst
        include .lgtm MAINTAINERS AUTHORS.rst
        include .lgtm
        include .MAINTAINERS RELEASE-NOTES.rst
        include RELEASE-NOTES.rst
        recursive-include * RELEASE-NOTES.rst
        recursive-include RELEASE-NOTES.rst
        recursive-exclude * *.py[co] .lgtm
        recursive-exclude * *.py[co] .lgtm MAINTAINERS
        recursive-exclude * __pycache__""")

    expected1 = dedent("""\
        include AUTHORS.rst
        recursive-include *
        recursive-exclude * *.py[co]
        recursive-exclude * *.py[co]
        recursive-exclude * __pycache__""")

    out = update_manifest_in(expected1)
    assert out == expected1
