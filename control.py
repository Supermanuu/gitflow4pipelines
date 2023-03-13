#!/usr/bin/env python

import os

import version
import project


def defaultIfNone(s, default = ''):
    return default if s == None else s


def getControlFile():
    # Version variables
    user_id = os.getenv('USER_ID') # Name for non CI versions
    build_id = os.getenv('BUILD_ID') # Local or CI version
    project_name_suffix = os.getenv('DEB_PROJECT_SUFFIX') # Project name suffix

    section = os.getenv('PACKAGE_SECTION')
    priority = os.getenv('PACKAGE_PRIORITY')
    maintainer = os.getenv('PACKAGE_MAINTAINER')
    architecture = os.getenv('PACKAGE_ARCHITECTURE')
    package_pre_depends = os.getenv('PACKAGE_PRE_DEPENDS')
    package_depends = os.getenv('PACKAGE_DEPENDS')
    package_conflicts = os.getenv('PACKAGE_CONFLICTS')
    package_replaces = os.getenv('PACKAGE_REPLACES')
    package_description = os.getenv('PACKAGE_DESCRIPTION')

    return '\
Package: ' + project.get_name(project_name_suffix) + '\n\
Version: ' + version.format_version(version.get_version(build_id=build_id), deb_version=True, user_id=user_id) + '\n\
Section: ' + defaultIfNone(section, 'apps') + '\n\
Priority: ' + defaultIfNone(priority, 'optional') + '\n\
Maintainer: ' + defaultIfNone(maintainer, 'SEDECAL') + '\n\
Architecture: ' + defaultIfNone(architecture) + '\n\
Pre-Depends: ' + defaultIfNone(package_pre_depends) + '\n\
Depends: ' + defaultIfNone(package_depends) + '\n\
Conflicts: ' + defaultIfNone(package_conflicts) + '\n\
Replaces: ' + defaultIfNone(package_replaces) + '\n\
Homepage: ' + project.get_url() + '\n\
Description: ' + defaultIfNone(package_description) + '\n'


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w') as writer:
            writer.writelines(getControlFile())
    else:
        print(getControlFile())
