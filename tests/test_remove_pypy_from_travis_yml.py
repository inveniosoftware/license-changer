from textwrap import dedent
from utils import remove_pypy_from_travis_yml


def test_remove_pypy_from_travis_yml():
    text = dedent("""\
    python:
      - "2.6"
      - "pypy"

    matrix:
      fast_finish: true
      allow_failures:
        - python: pypy

    before_install:
    """)

    expected = dedent("""\
    python:
      - "2.6"

    matrix:
      fast_finish: true

    before_install:
    """)

    out = remove_pypy_from_travis_yml(text)
    assert out == expected

    text = dedent("""\
    matrix:
      fast_finish: true
      allow_failures:
        - python: pypy
      include:
        - python: pypy
          env: EXTRAS=all,sqlite REQUIREMENTS=release SQLALCHEMY_DATABASE_URI="sqlite:///test.db" ES_HOST=127.0.0.1 ES_VERSION=2.2.0
    """)

    expected = dedent("""\
    matrix:
      fast_finish: true
      include:
          env: EXTRAS=all,sqlite REQUIREMENTS=release SQLALCHEMY_DATABASE_URI="sqlite:///test.db" ES_HOST=127.0.0.1 ES_VERSION=2.2.0
    """)

    import ipdb; ipdb.set_trace()
    out = remove_pypy_from_travis_yml(text)
    assert out == expected
