import sys
import re

def main():
    filename = sys.argv[1]

    with open(filename, 'r') as fp:
        content = fp.read()

    pkg_name = re.search(r'(.*)(travis\/inveniosoftware\/)(.*)(.svg)(.*)', content).groups()[2]
    badge_lines = [
        "",
        ".. image:: https://img.shields.io/github/license/inveniosoftware/{pkg_name}.svg".format(pkg_name=pkg_name),
        "        :target: https://github.com/inveniosoftware/{pkg_name}/blob/master/LICENSE".format(pkg_name=pkg_name),
        ]

    lines = content.split('\n')
    last_img_idx = next(idx for idx, l in reversed(list(enumerate(lines))) if l.startswith('.. image'))
    new_lines = lines[:last_img_idx+2] + badge_lines + lines[last_img_idx+2:]
    new_out = "\n".join(new_lines)

    with open(filename, 'w') as fp:
        content = fp.write(new_out)
main()
