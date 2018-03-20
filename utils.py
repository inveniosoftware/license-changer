import re
## Compiled regular expression pattern
## setup.py
RE_DEV_STATUS = re.compile(r"(.*)('Development Status ::.*')(.*)")
RE_INVENIO_DEV_DEP = re.compile(r"(?P<prefix>.*)(?P<invenio>invenio-.*)(?P<ver>1.0.0)(?P<devver>\.?([ab]|dev)+[0-9]+)(?P<suffix>.*)")
RE_INVENIO_SEARCH_DEV_DEP = re.compile(r"(invenio_)(.*)( = )(.*)(1.0.0)([ab]+[0-9]{1,2})(.*)")

## README.rst
RE_README_TAG_BADGE = re.compile(r"(.*)(img.shields.io/pypi/dm/)(invenio-.*)")
RE_README_TAG_URL = re.compile(r"(.*)(pypi.python.org/pypi/)(invenio-.*)")

# Constants
TROVE_DEV_STATUS = "Development Status :: 5 - Production/Stable"

def filter_text(text, fn):
    return '\n'.join(filter(fn, text.split('\n')))

def map_text(text, fn):
    return '\n'.join(map(fn, text.split('\n')))

def remove_setup_py_pypi_classifier(text):
    def pypy_trove(line):
        return 'Implementation :: PyPy' not in line
    return filter_text(text, pypy_trove)


def update_setup_py_development_status(text):
    def dev_status(line):
        m = re.match(RE_DEV_STATUS, line)
        if m:
            return "{0}'{trove}'{2}".format(*m.groups(), trove=TROVE_DEV_STATUS)
        return line
    return map_text(text, dev_status)


def update_setup_py_invenio_dev_deps(text):
    def dev_dep(line):
        m = re.match(RE_INVENIO_DEV_DEP, line)
        if m:
            # Skip the 'devver' groups corresponding to 'a3' 'b3' '.dev'
            return "{prefix}{invenio}{ver}{suffix}".format(**m.groupdict())
        return line

    def dev_dep_search(line):
        m = re.match(RE_INVENIO_SEARCH_DEV_DEP, line)
        if m:
            return "{0}{1}{2}{3}{4}{6}".format(*m.groups())  # Skip the 'a3' 'b3', 'a13' etc.
        return line
    text = map_text(text, dev_dep)
    text = map_text(text, dev_dep_search)
    return text


def update_setup_py(text):
    functs = [
        remove_setup_py_pypi_classifier,
        update_setup_py_development_status,
        update_setup_py_invenio_dev_deps,
    ]
    for fn in functs:
        text = fn(text)
    return text


def remove_readme_rst_badges(text):
    matching = [
        'shields.io/github/tag',
        'shields.io/github/license',
    ]
    cnt = 0
    new_out = []
    for line in text.split('\n'):
        if any(m in line for m in matching):
            cnt = 3  # skip next 3 lines
        if cnt == 0:
            new_out.append(line)
        else:
            cnt -= 1
    return "\n".join(new_out)


def change_readme_rst_tag_badge(text):

    def badge_img(line):
        m = re.match(RE_README_TAG_BADGE, line)
        if m:
            return "{0}img.shields.io/pypi/v/{2}".format(*m.groups())
        return line

    def badge_target(line):
        m = re.match(RE_README_TAG_URL, line)
        if m:
            return "{0}pypi.org/pypi/{2}".format(*m.groups())  # Skip the 'a3' 'b3', 'a13' etc.
        return line
    text = map_text(text, badge_img)
    text = map_text(text, badge_target)
    return text

def update_readme_rst(text):
    functs = [
        remove_readme_rst_badges,
        change_readme_rst_tag_badge,
    ]
    for fn in functs:
        text = fn(text)
    return text
