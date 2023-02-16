#!/usr/bin/env python

import re

from execute_shell import execute_shell

def get_url():
    urlOutput = execute_shell('git remote get-url origin')
    if len(urlOutput) == 1:
        return urlOutput[0]
    else:
        raise RuntimeError('Cannot determine git remote url')


def get_name():
    projectNamePattern = re.compile(r'^.*/([^/]+)$')
    found = projectNamePattern.match(get_url())
    if found == None:
        raise RuntimeError('Cannot determine repo name from URL')
    else:
        return found.group(1)


if __name__ == '__main__':
    print(get_name())
