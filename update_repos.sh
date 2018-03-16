#!/bin/sh

# Directory of the license-changer repository
CHANGER_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# This changes license in every file and commits the changes
change_license () {
    TEMPDIR=$1 repo=$2
    for file in $(git ls-files)
    do
        if [[ $repo == invenio* ]]; then
            $CHANGER_DIR/change_license.py $file &> /dev/null
        else
            # Pass repository name as second parameter (license formatting)
            # if it's not invenio-*
            $CHANGER_DIR/change_license.py $file $repo &> /dev/null
        fi
    done
    git commit -a -m 'global: license change to MIT License' --author='Invenio <info@inveniosoftware.org>' --no-gpg-sign &> /dev/null
    $CHANGER_DIR/clean_files.py setup.py &> /dev/null
    git commit -a -m 'installation: removed pytest-cache dependency' --author='Invenio <info@inveniosoftware.org>' --no-gpg-sign &> /dev/null
    $HOME/src/license-changer/update_travis.py .travis.yml
    git commit -a -m 'global: add allow_failures to travis config' --author='Invenio <info@inveniosoftware.org>' --no-gpg-sign &> /dev/null
    git grep -n "distributed in the hope that" | cat
    git grep -n "GPL" | cat
}

# This deletes files passed as argument and commits the changes
delete_files () {
    num_of_files_deleted=0
    declare -a files=("$@")

    for file in "${files[@]}";
    do
        if [ -f $file ]; then
            rm $file
            num_of_files_deleted=$((num_of_files_deleted + 1))
        fi
    done

    if [ $num_of_files_deleted -gt 0 ]; then
        git commit -a -m 'global: remove unused files' --author='Invenio <info@inveniosoftware.org>' --no-gpg-sign &> /dev/null
    else
        echo "No files to delete in this repository"
    fi
}

# This edits the CHANGES.rst file adding only the release 1.0.0
edit_changes_file () {
    cp $CHANGER_DIR/templates/changes_template.rst CHANGES.rst
    git add CHANGES.rst
    git commit -a -m 'global: prepared CHANGES.rst file for initial release' --author='Invenio <info@inveniosoftware.org>' --no-gpg-sign &> /dev/null
}

# This copies the CONTRIBUTING.rst file from invenio to every repo from inveniosoftware
update_contributing_file () {
    cp $CHANGER_DIR/templates/contributing_template.rst CONTRIBUTING.rst
    git add CONTRIBUTING.rst
    git commit -a -m 'global: harmonize contributing guidelines' --author='Invenio <info@inveniosoftware.org>' --no-gpg-sign &> /dev/null
}

main () {
    # This creates a directory in $HOME/$TEMPDIR  (see below)
    TEMPDIR="tmpsrc"
    if [ ! -d "$HOME/$TEMPDIR" ]; then
        mkdir $HOME/$TEMPDIR
    fi
    declare -a repos=(
        "dcxml"
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
        "invenio-i18n"
    )

    declare -a delfiles=(
        .lgtm
    )

    declare -a keepreleasenotes=(
        "dcxml"
        "citeproc-py-styles"
        "invenio-search-js"
    )

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

        change_license $TEMPDIR $repo
        delete_files "${delfiles[@]}"

        # Delete and sync release notes, but exclude some repositories
        del_rel_notes=1
        for repo2 in "${keepreleasenotes[@]}"
        do
            if [[ $repo == $repo2 ]]; then
                del_rel_notes=0
                break
            fi
        done
        if [ $del_rel_notes -gt 0 ]; then
            delete_files "${delfilesinvenio[@]}"
            edit_changes_file $repo
            echo "Updated release notes and changes file" $repo
        fi
        # TODO: Contributing guide temporarily disabled
        # update_contributing_file
    done

    echo "All repos UPDATED"
}

main
