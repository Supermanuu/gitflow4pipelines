#!/usr/bin/env python3

import os
import version
import project


def defaultIfNone(s : str, default : str = '') -> str:
    return default if s == None else s


def getControlFile() -> str:
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
Package: ' + project.getName() + '\n\
Version: ' + version.getVersion() + '\n\
Section: ' + defaultIfNone(section, 'apps') + '\n\
Priority: ' + defaultIfNone(priority, 'optional') + '\n\
Maintainer: ' + defaultIfNone(maintainer, 'SEDECAL') + '\n\
Architecture: ' + defaultIfNone(architecture) + '\n\
Pre-Depends: ' + defaultIfNone(package_pre_depends) + '\n\
Depends: ' + defaultIfNone(package_depends) + '\n\
Conflicts: ' + defaultIfNone(package_conflicts) + '\n\
Replaces: ' + defaultIfNone(package_replaces) + '\n\
Homepage: ' + project.getURL() + '\n\
Description: ' + defaultIfNone(package_description)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'w') as writer:
            writer.writelines(getControlFile())
    else:
        print(getControlFile())
