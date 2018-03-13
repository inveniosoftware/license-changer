# -*- coding: utf-8 -*-
"""Example setup.py file for testing purposes."""


from setuptools import find_packages, setup

tests_require = [
    'Flask-CeleryExt>=0.2.2',
    'Flask-Mail>=0.9.1',
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'mock>=2.0.0',
    'pydocstyle>=1.0.0',
    'pytest-cov>=1.8.0',
    'pytest-flask>=0.10.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
    'selenium>=3.0.1',
]

extras_require = {
    'tests': tests_require,
}

extras_require['all'] = []
for name, reqs in extras_require.items():
    if name[0] == ':':
        continue
    if name in ('mysql', 'postgresql', 'sqlite'):
        continue
    extras_require['all'].extend(reqs)

setup_requires = [
    'Babel>=1.3',
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask-BabelEx>=0.9.3',
    'Flask-Breadcrumbs>=0.3.0',
    'Flask-KVSession>=0.6.1',
    'Flask-Login>=0.3.0',
    'Flask-Menu>=0.4.0',
    'Flask-Security>=3.0.0',
    'Flask-WTF>=0.13.1',
    'Flask>=0.11.1',
    'SQLAlchemy-Utils>=0.31.0',
    'cryptography>=2.1.4',
    'invenio-i18n>=1.0.0b4',
    'redis>=2.10.5',
]

packages = find_packages()

setup(
    name='foo bar',
    version='1.0',
    description=__doc__,
    long_description=__doc__,
    keywords='foo bar',
    license='MIT',
    author='foo bar',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'foo': [
            'bar = baz',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
