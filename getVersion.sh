#!/bin/bash

set -e
ENV_FILE='/home/root/workdir/.env'

[ -z "$1" ] || PROJECT_NAME=${1}_
[ -z "$2" ] || ARCHITECTURE=_${2}

ls $ENV_FILE &>/dev/null || (echo "Env file not found on $ENV_FILE" && exit 1)

if [ "$READ" != "NO" ]; then
    PROJECT_VERSION_MAJOR=$(grep -Eo '^PROJECT_VERSION_MAJOR=[0-9]+' $ENV_FILE | grep -Eo '[0-9]+')
    PROJECT_VERSION_MINOR=$(grep -Eo '^PROJECT_VERSION_MINOR=[0-9]+' $ENV_FILE | grep -Eo '[0-9]+')
    PROJECT_VERSION_PATCH=$(grep -Eo '^PROJECT_VERSION_PATCH=[0-9]+' $ENV_FILE | grep -Eo '[0-9]+')
fi

[ -z "$PROJECT_VERSION_MAJOR" \
    -o -z "$PROJECT_VERSION_MINOR" \
    -o -z "$PROJECT_VERSION_PATCH" ] && (echo "Bad env file" && exit 2)

echo ${PROJECT_NAME}${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}${ARCHITECTURE}
