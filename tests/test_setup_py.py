from utils import update_setup_py, update_setup_py_invenio_dev_deps
from textwrap import dedent

def test_pypy_classifier():
    text1 = """\
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Development Status :: 4 - Beta',"""

    exp_text1 = """\
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',"""
    assert update_setup_py(text1) == exp_text1
    assert update_setup_py(exp_text1) == exp_text1


def test_invenio_dev_deps():
    text1 = """\
        tests_require = [
            'Flask-CeleryExt>=0.2.2',
            'invenio-mail>=1.0.0a3',
            'invenio-oaiserver>=1.0.0a9',
            'isort>=4.3.3',
        """

    exp_text1 = """\
        tests_require = [
            'Flask-CeleryExt>=0.2.2',
            'invenio-mail>=1.0.0',
            'invenio-oaiserver>=1.0.0',
            'isort>=4.3.3',
        """
    assert update_setup_py_invenio_dev_deps(text1) == exp_text1
    assert update_setup_py_invenio_dev_deps(exp_text1) == exp_text1
    text2 = dedent("""\
        install_requires = [
            'Flask-BabelEx>=0.9.3',
            'Flask>=0.11.1',
            'elasticsearch-dsl>=2.0.0,<3.0.0',
            'elasticsearch>=2.0.0,<3.0.0',
            'invenio-access>=1.0.0a11',
            'invenio-accounts>=1.0.0b1',
            'invenio-assets>=1.0.0b2',
            'invenio-files-rest>=1.0.0.a14',  # Watch out for the dot ".a14"
            'invenio-indexer>=1.0.0a8',
            'invenio-pidstore>=1.0.0b1',
            'invenio-records>=1.0.0b1',
            'invenio-rest[cors]>=1.0.0a9',
            'invenio-records-ui>=1.0.0a8,<1.1.0',  # Upper-limiter
            'invenio-search>=1.0.0a9'
            'invenio-base>=1.0.0.dev20160101,<1.1.0',  # strip '.dev<date>'
            'invenio-app-ils>=1.0.0.dev0,<1.1.0',
        ]

        invenio_search_version = '1.0.0b3'  # comment
        invenio_db_version = '1.0.0a15'  # comment 2

        extras_require = {}
    """)
    exp_text2 = dedent("""\
        install_requires = [
            'Flask-BabelEx>=0.9.3',
            'Flask>=0.11.1',
            'elasticsearch-dsl>=2.0.0,<3.0.0',
            'elasticsearch>=2.0.0,<3.0.0',
            'invenio-access>=1.0.0',
            'invenio-accounts>=1.0.0',
            'invenio-assets>=1.0.0',
            'invenio-files-rest>=1.0.0',  # Watch out for the dot ".a14"
            'invenio-indexer>=1.0.0',
            'invenio-pidstore>=1.0.0',
            'invenio-records>=1.0.0',
            'invenio-rest[cors]>=1.0.0',
            'invenio-records-ui>=1.0.0,<1.1.0',  # Upper-limiter
            'invenio-search>=1.0.0'
            'invenio-base>=1.0.0,<1.1.0',  # strip '.dev<date>'
            'invenio-app-ils>=1.0.0,<1.1.0',
        ]

        invenio_search_version = '1.0.0'  # comment
        invenio_db_version = '1.0.0'  # comment 2

        extras_require = {}
    """)
    assert update_setup_py_invenio_dev_deps(text2) == exp_text2
    assert update_setup_py_invenio_dev_deps(exp_text2) == exp_text2
