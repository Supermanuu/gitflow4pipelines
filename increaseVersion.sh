#!/bin/bash

set -e
ENV_FILE='/home/root/workdir/.env'

ls $ENV_FILE &>/dev/null || (echo "Env file not found on $ENV_FILE" && exit 1)

export PROJECT_VERSION_MAJOR=$(grep -Eo '^PROJECT_VERSION_MAJOR=[0-9]+' $ENV_FILE | grep -Eo '[0-9]+')
export PROJECT_VERSION_MINOR=$(grep -Eo '^PROJECT_VERSION_MINOR=[0-9]+' $ENV_FILE | grep -Eo '[0-9]+')
export PROJECT_VERSION_PATCH=$(grep -Eo '^PROJECT_VERSION_PATCH=[0-9]+' $ENV_FILE | grep -Eo '[0-9]+')

[ -z "$PROJECT_VERSION_MAJOR" \
    -o -z "$PROJECT_VERSION_MINOR" \
    -o -z "$PROJECT_VERSION_PATCH" ] && (echo "Bad env file" && exit 2)

PROJECT_VERSION_PATCH=$(expr $PROJECT_VERSION_PATCH + 1)

if [ "$CHANGE" == 'YES' ]; then
    sed -i "s/PROJECT_VERSION_MAJOR=[0-9]\+/PROJECT_VERSION_MAJOR=$PROJECT_VERSION_MAJOR/g" $ENV_FILE
    sed -i "s/PROJECT_VERSION_MINOR=[0-9]\+/PROJECT_VERSION_MINOR=$PROJECT_VERSION_MINOR/g" $ENV_FILE
    sed -i "s/PROJECT_VERSION_PATCH=[0-9]\+/PROJECT_VERSION_PATCH=$PROJECT_VERSION_PATCH/g" $ENV_FILE
fi

READ="NO" /getVersion.sh "$@"
