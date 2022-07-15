#!/usr/bin/env python3

import re
import subprocess

def sortTag(tag):
    return [int(i) if i.isdigit() else i for i in organizer(tag)]

def sortTags(tags):
    return sorted(tags, key=sortTag)

def organizer(tag):
    # order: major, minor, patch, revision, build
    splittedTag = tag.replace('r','.').replace('-','.').split('.')
    if 'r' not in tag:
        splittedTag.insert(0,'0') # by default 0 revision
    if '-' not in tag:
        splittedTag.append('0') # by default 0 build
    splittedTag.insert(3, splittedTag.pop(0))
    splittedTag[4] = re.sub("[^0-9]", "", splittedTag[4]) # to avoid digit to string comparison and string to string comparison
    return splittedTag

def prettyTag(tag):
    return tag.replace("r",":")

def get():
    tags = subprocess.check_output(["git", "tag", "--merged"]).decode("utf8").split("\n")
    tags.remove("")
    return prettyTag(sortTags(tags)[-1])

if __name__ == '__main__':
        print(get())
