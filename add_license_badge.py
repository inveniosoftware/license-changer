import sys
import re

def main():
    filename = sys.argv[1]

    with open(filename, 'r') as fp:
        content = fp.read()

    pos = content.find('.. image')
    pkg_name = re.search(r'(.*)(travis\/inveniosoftware\/)(.*)(.svg)(.*)', content).groups()[2]
    fmt = (".. image:: https://img.shields.io/github/license/inveniosoftware/{pkg_name}.svg\n"
           "        :target: https://github.com/inveniosoftware/{pkg_name}/blob/master/LICENSE\n\n")
    shield = fmt.format(pkg_name=pkg_name)
    new_out = content[:pos] + shield + content[pos:]

    with open(filename, 'w') as fp:
        content = fp.write(new_out)
main()
