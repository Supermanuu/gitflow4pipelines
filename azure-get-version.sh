set -e

# TODO: remove
echo $FIX $HOTFIX

echo 'Select version increase'
[ "$FIX" = "True" ] && INCREASE='--fix'
[ "$HOTFIX" = "True" ] && INCREASE='--hotfix'
[ -z "$INCREASE" ] && INCREASE='--next'

echo 'Get versions'
VERSION=$(docker compose run --rm version version.py -p $(Build.Repository.Name))
NEW_VERSION=$(docker compose run --rm version version.py -p $(Build.Repository.Name) $INCREASE)

echo "Current version: $VERSION"
echo "Next version: $NEW_VERSION"

echo 'Returns this variables to YAML pipeline'
echo "##vso[task.setvariable variable=Version;]$VERSION"
echo "##vso[task.setvariable variable=NewVersion;]$NEW_VERSION"
