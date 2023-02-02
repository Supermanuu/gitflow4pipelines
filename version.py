#!/usr/bin/env python3

import os
import re
import subprocess

import project


debug = os.getenv('DEBUG')
user_id = os.getenv('USER_ID') # Name for non CI versions
build_id = os.getenv('BUILD_ID') # Local or CI version
deb_version = os.getenv('DEB_VERSION') # DEB version formatting
project_name = os.getenv('DEB_PROJECT') # Project name
architecture = os.getenv('DEB_ARCHITECTURE') # Binary architecture

# Version format:
#   \d+ . \d+ . \d+ [ . \d+ ] [ \+   \w+   ]
#   major minor patch revision  special name
# 
# Release format:
#  release/ \d+ . \d+ . \d+ [ . \d+ ] [ \+   \w+   ]
#           major minor patch revision  special name
versionPattern = re.compile(r'^(\d+\.\d+\.\d+)(\.\d+)?(\+\w+)?$')
releasePattern = re.compile(r'^release/((?:\d+\.\d+\.\d+)(?:\.\d+)?(?:\+\w+)?)$')


class ReleaseIsNotNormalized(RuntimeError):
    '''Raised when the release branch dont follow the specified pattern'''
    pass


def debugm(message : str):
    '''Print this message on debug run'''
    if debug: print(message)


def debVersioning(version : str):
    '''Converts this version to Debian versioning format'''
    found = versionPattern.match(version)
    if found == None:
        raise RuntimeError('Bad formatted version: \'' + version + '\'. It must follow ' + versionPattern.pattern)
    else:
        revision = found.group(2).replace('.', '') + ":" if found.group(2) != None else ''
        additional = found.group(3) if found.group(3) != None else ''
        return revision + found.group(1) + additional


def getVersionFromCurrentBranch(branch : str):
    '''Version from branch name'''
    debugm('Checking \'' + branch + '\'')
    found = releasePattern.match(branch)
    if found == None:
        raise ReleaseIsNotNormalized('This branch does not follow the naming convention ' + releasePattern.pattern)
    else:
        return found.group(1)


def getFirstNormalizedVersion():
    '''Branch name from this git branch, iterate until first good named branch'''
    # Get all references from this commit
    refs = subprocess.check_output('git rev-list HEAD'.split(' ')).decode('UTF-8').split('\n')
    refs.remove('')
    if len(refs) == 0:
        raise RuntimeError('No refs found')
    else:
        for ref in refs:
            debugm('Checking ' + ref)
            # Get all branches that contains this reference
            branchesCommand = 'git branch --contains ' + ref
            branches = subprocess.check_output(branchesCommand.split(' ')).decode('UTF-8').split('\n')
            branches.remove('')
            branches.reverse()
            debugm(branches)
            if len(branches) == 0:
                print('No related branches for \'' + branchesCommand + '\'')
            else:
                for branch in branches:
                    # Check each branch in order
                    try:
                        return getVersionFromCurrentBranch(branch.replace('  ', '').replace('* ', ''))
                    except ReleaseIsNotNormalized:
                        pass


def getVersion() -> str:
    # Branch name from this git branch, else iterate until first good named branch
    thisBranch = subprocess.check_output('git rev-parse --abbrev-ref HEAD'.split(' ')).decode('UTF-8').split('\n')
    thisBranch.remove('')
    if len(thisBranch) > 0:
        try:
            version = getVersionFromCurrentBranch(thisBranch[0])
        except ReleaseIsNotNormalized: 
            version = getFirstNormalizedVersion()

    if version == None:
        raise RuntimeError('No version could be parsed')

    if deb_version != None:
        version = debVersioning(version)
    if build_id != None:
        if '+' in version:
            # Build id just before -
            splittedVersion = version.split('+')
            version = splittedVersion[0] + '-' + build_id + '+' + splittedVersion[1]
        else:
            version += '-' + build_id
    if user_id != None:
        version += '+' + user_id
    if architecture != None:
        version += '_' + architecture
    if project_name != None:
        version = project.getName() + '_' + version
    return version


if __name__ == '__main__':
    print(getVersion())
