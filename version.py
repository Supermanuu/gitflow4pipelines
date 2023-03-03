#!/usr/bin/env python

import os
import re
import sys

import project
from execute_shell import execute_shell


# Version format:
#   \d+ . \d+ . \d+ [ . \d+ ] [ \+   \w+   ]
#   major minor patch revision  identifier
# 
# Release format:
#  release/ \d+ . \d+ . \d+ [ . \d+ ] [ \+   \w+   ]
#           major minor patch revision  identifier
global_version_pattern = re.compile(r'^(\d+)\.(\d+)\.(\d+)((?:\.\d+)?)((?:-\d+)?)((?:\+\w+)?)$')
global_release_pattern = re.compile(r'^(?:remotes/origin/)?release/((?:\d+\.\d+\.\d+)(?:\.\d+)?(?:\+\w+)?)$')
global_debug = os.getenv('DEBUG')


class ReleaseIsNotNormalized(RuntimeError):
    '''Raised when the release branch dont follow the specified pattern'''
    pass


def debugm(message):
    '''Print this message on debug run'''
    if global_debug: print(message)


def split_version(version):
    '''
    Parses a version and returns a dictionary with major, minor, patch, revision and identifier

    Immportant notes:
        Revision and identifier can be empty strings if they are not present on version
        Build id is not present cause it never can be found on a git release branch name
    '''
    found = global_version_pattern.match(version)
    if found == None:
        raise RuntimeError('Bad formatted version: \'' + version + '\'. It must follow ' + global_version_pattern.pattern)
    else:
        return {
            'major': found.group(1),
            'minor': found.group(2),
            'patch': found.group(3),
            'revision': found.group(4).replace('.',''),
            'build': found.group(5).replace('-',''),
            'identifier': found.group(6) 
        }


def get_version_from_current_branch(branch):
    '''Version from branch name'''
    debugm('Checking \'' + branch + '\'')
    found = global_release_pattern.match(branch)
    if found == None:
        raise ReleaseIsNotNormalized('This branch does not follow the naming convention ' + global_release_pattern.pattern)
    else:
        return split_version(found.group(1))


def get_first_normalized_version():
    '''Branch name from this git branch, iterate until first good named branch'''
    # Get all references from this commit
    refs = execute_shell('git rev-list HEAD')
    if len(refs) == 0:
        raise RuntimeError('No refs found')
    else:
        for ref in refs:
            debugm('Checking ' + ref)
            # Get all branches that contains this reference
            branchesCommand = 'git branch -a --sort=-committerdate --contains ' + ref
            branches = execute_shell(branchesCommand)
            branches.reverse()
            debugm(branches)
            if len(branches) == 0:
                print('No related branches for \'' + branchesCommand + '\'')
            else:
                for branch in branches:
                    # Check each branch in order
                    try:
                        return get_version_from_current_branch(branch.replace('  ', '').replace('* ', ''))
                    except ReleaseIsNotNormalized:
                        pass


def get_version():
    # Branch name from this git branch, else iterate until first good named branch
    thisBranch = execute_shell('git rev-parse --abbrev-ref HEAD')
    if len(thisBranch) > 0:
        try:
            version = get_version_from_current_branch(thisBranch[0])
        except ReleaseIsNotNormalized: 
            version = get_first_normalized_version()

    if version == None:
        raise RuntimeError('No version could be parsed')

    return version

def format_version(version, deb_version = False, build_id = None, user_id = None, architecture = None, project_name = False, project_name_suffix = None):
    '''Takes a version dictionary and generates a string'''
    version_string = ''

    # Deb revision special case
    if version['revision'] != '' and deb_version:
        version_string += version['revision'] + ":" if version['revision'] != '' else ''
    
    # Core version
    version_string += version['major'] + '.' + version['minor'] + '.' + version['patch']

    # Normal revision
    if version['revision'] != '' and not deb_version:
            version_string += '.' + version['revision']

    # Build ID
    if build_id != None:
            version_string += '-' + build_id

    # Identifier
    version_string += version['identifier']

    # User ID
    if user_id != None:
        version_string += '+' + user_id

    # Architecture and project for deb version
    if deb_version:
        if architecture != None:
            version_string += '_' + architecture
        if project_name:
            version_string = project.get_name(project_name_suffix) + '_' + version_string
    
    return version_string


if __name__ == '__main__':
    # Arguments
    if sys.version_info[0] == 2:
        from dotdict import Dotdict
        if len(sys.argv) > 1:
            args = Dotdict({
                'major'     : sys.argv[1] == '-1' or sys.argv[1] == '--major',
                'minor'     : sys.argv[1] == '-2' or sys.argv[1] == '--minor',
                'patch'     : sys.argv[1] == '-3' or sys.argv[1] == '--patch',
                'revision'  : sys.argv[1] == '-4' or sys.argv[1] == '--revision',
                'build'     : sys.argv[1] == '-5' or sys.argv[1] == '--build'
            })
        else:
            args = Dotdict({
                'major'     : False,
                'minor'     : False,
                'patch'     : False,
                'revision'  : False,
                'build'     : False
            })
    else:
        import argparse
        parser = argparse.ArgumentParser(description='Manages the version change through git.')
        show = parser.add_mutually_exclusive_group()
        show.add_argument('-1', '--major'   , action="store_true", help='Shows major version')
        show.add_argument('-2', '--minor'   , action="store_true", help='Shows minor version')
        show.add_argument('-3', '--patch'   , action="store_true", help='Shows patch version')
        show.add_argument('-4', '--revision', action="store_true", help='Shows revision version')
        show.add_argument('-5', '--build'   , action="store_true", help='Shows build version')
        show.add_argument('-t', '--tag'     , action="store_true", help='Iterate over tags instead of branches')
        args = parser.parse_args(sys.argv[1:])

    # Environment variables
    user_id = os.getenv('USER_ID') # Name for non CI versions
    build_id = os.getenv('BUILD_ID') # Local or CI version
    deb_version = os.getenv('DEB_VERSION') # DEB version formatting
    project_name = os.getenv('DEB_PROJECT') # Project name
    project_name_suffix = os.getenv('DEB_PROJECT_SUFFIX') # Project name suffix
    architecture = os.getenv('PACKAGE_ARCHITECTURE') # Binary architecture

    version = get_version()
    if args.major:
        print(version['major'])
    elif args.minor: 
        print(version['minor'])
    elif args.patch: 
        print(version['patch'])
    elif args.build: 
        print(build_id if build_id != None else 0)
    elif args.revision: 
        print(version['revision'] if version['revision'] != '' else 0)
    else:
        print(format_version(version, deb_version != None, build_id, user_id, architecture, project_name != None, project_name_suffix))
