#!/usr/bin/env python3

import re
import subprocess

def getURL() -> str:
    urlOutput = subprocess.check_output('git remote get-url origin'.split(' ')).decode('UTF-8').split('\n')
    urlOutput.remove('')
    if len(urlOutput) == 1:
        return urlOutput[0]
    else:
        raise RuntimeError('Cannot determine git remote url')


def getName():
    projectNamePattern = re.compile(r'^.*/([^/]+)$')
    found = projectNamePattern.match(getURL())
    if found == None:
        raise RuntimeError('Cannot determine repo name from URL')
    else:
        return found.group(1)


if __name__ == '__main__':
    print(getName())
