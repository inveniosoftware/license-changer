# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Application bootstraping."""

from __future__ import absolute_import, print_function

import warnings

import click
from flask import current_app
from flask.cli import with_appcontext
from pkg_resources import iter_entry_points, resource_filename, working_set


@click.group()
def instance():
    """Instance commands."""

# Even more
# top-level
# block comments

def main():
    pass
