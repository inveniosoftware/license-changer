from collections import defaultdict
from datetime import datetime

import yaml
from github3 import GitHub

# for d in ./* ; do ( cd $d && if git log --pretty=oneline | grep 'global: initial package separation' ; then echo $d ; fi  ) ; done
base_commits = {
    'invenio': 'c4c292f9b3c3aaf65ea20cb74e4f3ec8ae4adcd9',
    'invenio-access': '5b2818387c9f833438fa30f67d47f529ecaa0968',
    'invenio-accounts': 'f97176828348baeb32bf9556001112ba49bcf4b2',
    'invenio-base': 'd8e31ee5f0e808a9b4cf37d9a987636e53439f32',
    'invenio-celery': '23dd4cdcc9699ae1a550d024055afbfbe34195ef',
    'invenio-collections': '99d5df278e5d6981d2a0c19c3abf90c29dcd005d',
    'invenio-communities': 'c76f30d38c69cb593edd97fee4d5cd690bcd136c',
    'invenio-deposit': 'aa654f01f9a9bd5b6ec19ae53326f04c4b1b1740',
    'invenio-formatter': '0733556a2fb8d7c524464b64c4de8b0e2ad0a246',
    'invenio-oaiharvester': 'a4325a61bc71a4aa4691d673a4bf4449671966f0',
    'invenio-oauth2server': '094323a759b837272d4a77a7141e80012939782f',
    'invenio-oauthclient': '7adadb59eab1dde241d2f041088dc79c1e190a56',
    'invenio-pages': '5f46a3c7194c5ef27f26c04699aa37a6c797afb2',
    'invenio-pidstore': 'b44142197566ef2ab6ecbed6d75dafd1e14da41b',
    'invenio-previewer': 'ede10b7f6172f81dda3a9f6695217892897dda08',
    'invenio-records': 'a685b1d0e0d62798619f3e084605bf42281b1f1c',
    'invenio-search': '1cd5740aae6022ffb0a781c3d63dd3b26b83dc61',
    'invenio-sequencegenerator': '1b55943e1f5e8dbf992b9d44412b2a783c415068',
    'invenio-webhooks': '43e2f1e7670781d57f7d1cf9c03bdf91f9afe23b',
}

link_search_name = 'https://github.com/inveniosoftware/{0}/search?q=author-name:{1}&type=Commits'
link_search_login = 'https://github.com/inveniosoftware/{0}/commits?author={1}'

with open('./people.yaml') as f:
    people = yaml.load(f)

cern_people = set(p for k, g in people.items() if 'cern' in k for p in g)
external = defaultdict(lambda: defaultdict(list))

g = GitHub(token='<token>')
org = g.organization('inveniosoftware')

for repo in org.repositories():
    if repo.fork or 'flask' in repo.name.lower():
        # Remove forks and flask packages
        # flask-menu
        # flask-breadcrumbs
        # flask-sso
        # flask-iiif
        # flask-sitemap
        # flask-cli
        # flask-celeryext
        # flask-security-fork
        # flask-webpackext
        continue
    if repo.name in base_commits:
        commit = repo.commit(base_commits[repo.name])
        since = datetime.strptime(commit.last_modified,
                                  '%a, %d %b %Y %H:%M:%S %Z')
        commits = repo.commits(since=since)
    else:
        commits = repo.commits()

    contributors = defaultdict(
        lambda: {'count': 0, 'link_search': '', 'cern': False})

    for commit in commits:
        try:
            key = commit.author.login
            link_search = link_search_login.format(repo.name, key)
        except AttributeError:
            key = commit.commit.author['name']
            link_search = link_search_name.format(repo.name, key)

        contributors[key]['count'] += 1
        contributors[key]['link_search'] = link_search
        contributors[key]['cern'] = key in cern_people

        if not contributors[key]['cern']:
            external[key][repo.name].append(commit)

    with open('./{0}.md'.format(repo.name), 'w') as f:
        for name, info in sorted(
                contributors.items(),
                key=lambda c: (c[1]['cern'], c[0].lower())):
            f.write('* {0}\n'.format(name))
            f.write(
                '  * External: {0}\n'.format('NO' if info['cern'] else 'YES'))
            f.write('  * Commit count: {0}\n'.format(info['count']))
            f.write('  * [See all commits]({0})\n'.format(info['link_search']))

for name, info in external.items():
    with open('./{0}.md'.format(name), 'w') as f:
        for repo, commits in info.items():
            f.write('# {0}\n'.format(repo))
            f.writelines([
                '* [{0}]({1}) {3}'.format(c.sha, c.html_url, c.last_modified,
                                          c.message.splitlines()[0])
                for c in commits
            ])
            f.write('\n\n')
