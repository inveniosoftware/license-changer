#!/bin/sh

# Directory of the license-changer repository
CHANGER_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

main () {
    # This creates a directory in $HOME/$TEMPDIR  (see below)
    TEMPDIR="tmpsrc"
    if [ ! -d "$HOME/$TEMPDIR" ]; then
        mkdir $HOME/$TEMPDIR
    fi
    declare -a repos=(
        ### Initial repositories on the list stuff
        #"dcxml"
        #"citeproc-py-styles"
        #"invenio-marc21"
        #"invenio-theme"
        #"invenio-search-js"
        #"invenio-search-ui"
        #"invenio-search"
        #"invenio-rest"
        #"invenio-records-ui"
        #"invenio-records"
        #"invenio-pidstore"
        #"invenio-oauthclient"
        #"invenio-oauth2server"
        #"invenio-logging"
        #"invenio-formatter"
        "invenio-db"
        #"invenio-config"
        #"invenio-celery"
        #"invenio-cache"
        #"invenio-base"
        #"invenio-assets"
        #"invenio-app"
        #"invenio-admin"
        #"invenio-accounts"
        #"invenio-access"
        #"invenio-userprofiles"
        #"invenio-records-rest"
        #"invenio-oaiserver"
        #"invenio-mail"
        #"invenio-jsonschemas"
        #"invenio-indexer"
        #"invenio-i18n"
    )

    for repo in "${repos[@]}"
    do
        if [ ! -d "$HOME/$TEMPDIR/$repo" ]; then
            echo $repo "FETCHING"
            cd "$HOME/$TEMPDIR"
            git clone "git@github.com:inveniosoftware/${repo}.git" &> /dev/null
        fi
        cd "$HOME/$TEMPDIR/$repo"

        if [ -d "$HOME/$TEMPDIR/$repo/docs" ]; then
            # Skip last 4 lines
            head -n -4 LICENSE > LICENSE2
            mv LICENSE2 LICENSE
            cat $CHANGER_DIR/license_rst_note >> $HOME/$TEMPDIR/$repo/docs/license.rst
            python $HOME/$TEMPDIR/$repo/README.rst
        else
            echo "There's no docs/. Skipping" $repo
        fi

        # git commit -a -m 'global: Updated AUTHORS.rst' --author='Invenio <info@inveniosoftware.org>' --no-gpg-sign &> /dev/null

        # TODO: uncomment for actual live run
        # git push origin release-1.0.0 --force
    done

    echo "All repos UPDATED"
}

main
