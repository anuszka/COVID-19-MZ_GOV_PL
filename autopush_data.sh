#!/bin/sh
###########################
#cd .
# switch to branch you want to use
git checkout master
# add all added/modified files
git add .
# commit changes
git commit -am "update"
# push to git remote repository
git push
###########################
echo Press Enter...
read