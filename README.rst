=================
 License changer
=================

This repository contains helper utilities for changing the license of Invenio
source code files.

Usage::

  $ cd private/src/invenio-oaiserver
  $ git checkout -b license-change
  $ for file in $(git ls-files); do change_license $file; done
  $ git commit -a -s -m 'global: license change to MIT License'
  $ git grep 'distributed in the hope that'
