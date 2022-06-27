set -e
echo "Setting user and email"
git config --global user.name "Build Service"
git config --global user.email "buildservice@buildservice.buildservice"
echo "Getting development"
git checkout development
git reset --hard origin/development # removes staged and working directory changes
git clean -f -d # remove untracked
git pull
echo "Increasing version"
[ "$FIX" = "True" ] && INCREASE='--fix'
[ "$HOTFIX" = "True" ] && INCREASE='--hotfix'
[ -z "$INCREASE" ] && INCREASE='--next'
NEW_VERSION=$(docker compose run --rm version version.py -p $(Build.Repository.Name) $INCREASE -w)
echo "Committing new version $NEW_VERSION"
git add .env
git commit -m "Generated new version $NEW_VERSION [skip ci]"
git push
echo "Tagging version to $NEW_VERSION"
git tag -a $NEW_VERSION -m "New version avaliable"
git push origin $NEW_VERSION
