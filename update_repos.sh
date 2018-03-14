#
# This creates a directory in $HOME/$TEMPDIR  (see below)
#
TEMPDIR="tmpsrc"
if [ ! -d "$HOME/$TEMPDIR" ]; then
    mkdir $HOME/$TEMPDIR
fi
declare -a repos=("dcxml"
                  "citeproc-py-styles"
                  "invenio-marc21"
                  "invenio-theme"
                  "invenio-search-js"
                  "invenio-search-ui"
                  "invenio-search"
                  "invenio-rest"
                  "invenio-records-ui"
                  "invenio-records"
                  "invenio-pidstore"
                  "invenio-oauthclient"
                  "invenio-oauth2server"
                  "invenio-logging"
                  "invenio-formatter"
                  "invenio-db"
                  "invenio-config"
                  "invenio-celery"
                  "invenio-cache"
                  "invenio-base"
                  "invenio-assets"
                  "invenio-app"
                  "invenio-admin"
                  "invenio-accounts"
                  "invenio-access"
                  "invenio-userprofiles"
                  "invenio-records-rest"
                  "invenio-oaiserver"
                  "invenio-mail"
                  "invenio-jsonschemas"
                  "invenio-indexer"
                  "invenio-i18n")

for repo in "${repos[@]}"
do
    if [ ! -d "$HOME/$TEMPDIR/$repo" ]; then
        echo $repo "FETCHING"
        cd "$HOME/$TEMPDIR"
        git clone "git@github.com:inveniosoftware/${repo}.git" &> /dev/null
        cd $repo
        git remote rename origin upstream &> /dev/null
    fi
    cd "$HOME/$TEMPDIR/$repo"
    git checkout -b license-change &> /dev/null
    for file in $(git ls-files)
    do
        if [[ $repo == "invenio-*" ]]; then
            $HOME/src/license-changer/change_license.py $file &> /dev/null
        else
            # Pass repository name as second parameter (license formatting)
            # if it's not invenio-*
            $HOME/src/license-changer/change_license.py $file $repo &> /dev/null
        fi
    done
    $HOME/src/license-changer/clean_files.py setup.py &> /dev/null
    git commit -a -m 'global: license change to MIT License' --author='Invenio <info@inveniosoftware.org>' --no-gpg-sign &> /dev/null
    git grep -n "distributed in the hope that" | cat
    git grep -n "GPL" | cat
done
echo "All repos OK"
