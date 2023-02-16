#!/usr/bin/env python3

import re
import subprocess

def get_url() -> str:
    urlOutput = subprocess.check_output('git remote get-url origin'.split(' ')).decode('UTF-8').split('\n')
    urlOutput.remove('')
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
