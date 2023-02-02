#!/usr/bin/env python3

import re
import subprocess

def getProjectName():
    projectNamePattern = re.compile(r'^.*/([^/]+)$')
    projectNameOutput = subprocess.check_output('git remote get-url origin'.split(' ')).decode('UTF-8').split('\n')
    projectNameOutput.remove('')
    if len(projectNameOutput) == 1:
        found = projectNamePattern.match(projectNameOutput[0])
        if found == None:
            raise RuntimeError('Cannot determine repo name from ' + projectNameOutput[0])
        else:
            return found.group(1)
    else:
        raise RuntimeError('Cannot determine git remote URL')


if __name__ == '__main__':
    print(getProjectName())
