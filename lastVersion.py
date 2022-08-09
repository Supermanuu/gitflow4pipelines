#!/usr/bin/env python3

import re
import sys
import subprocess

tagCheck = re.compile(r"^\d+\.\d+\.\d+(?:\.\d+)?(?:-[\da-zA-Z_]+)?$")

def sortTags(tags):
    return sorted(tags, key=organizer)

def organizer(tag):
    # format: 1.2.3[.4][-5]
    if not tagCheck.match(tag):
        raise RuntimeError("Bad tag format")

    # order: major (1), minor (2), patch (3), revision (4), build (5)
    splittedBuild = tag.split('-')
    splittedTag = splittedBuild[0].split('.')
    if len(splittedTag) < 4:
        splittedTag.append('0') # by default 0 revision
    if len(splittedBuild) < 2:
        splittedTag.append('0') # by default 0 build
    else:
        splittedTag.append(splittedBuild[1])
    splittedTag[4] = re.sub("[^0-9]", "", splittedTag[4]) # to avoid digit to string comparison and string to string comparison
    return [int(i) for i in splittedTag]

def debTag(tag):
    splittedBuild = tag.split('-')
    splittedTag = splittedBuild[0].split(".")
    if len(splittedTag) > 3:
        splittedTag.insert(0, splittedTag.pop(3))
        splittedTag.insert(0, splittedTag.pop(0) + ":" + splittedTag.pop(0))
    joinedTag = ".".join(splittedTag)
    if len(splittedBuild) > 1:
        return "-".join([joinedTag, splittedBuild[1]])
    else:
        return joinedTag

def get():
    tags = subprocess.check_output(["git", "tag", "--merged"]).decode("utf8").split("\n")
    tags.remove("")
    sortedTags = sortTags(tags)
    print(f"Sorted tags: {sortedTags}", file=sys.stderr)
    return debTag(sortedTags[-1])

if __name__ == '__main__':
    print(get())
