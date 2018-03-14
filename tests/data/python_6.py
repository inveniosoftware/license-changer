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
