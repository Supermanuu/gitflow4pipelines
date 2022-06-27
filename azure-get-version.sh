set -e
echo $FIX $HOTFIX
[ "$FIX" = "True" ] && INCREASE='--fix'
[ "$HOTFIX" = "True" ] && INCREASE='--hotfix'
[ -z "$INCREASE" ] && INCREASE='--next'
VERSION=$(docker compose run --rm version version.py -p $(Build.Repository.Name))
NEW_VERSION=$(docker compose run --rm version version.py -p $(Build.Repository.Name) $INCREASE)
echo "Current version: $VERSION"
echo "Next version: $NEW_VERSION"
echo "##vso[task.setvariable variable=Version;]$VERSION"
echo "##vso[task.setvariable variable=NewVersion;]$NEW_VERSION"
