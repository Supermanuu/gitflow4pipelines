#!/usr/bin/env python3

import os
import re
import sys
import argparse
import subprocess

versions = re.compile(r'^PROJECT_VERSION_([^=]+)=([a-zA-Z0-9]+)(?: ?#.*)?$')

# Version format definition as known by the DEB package documentation
def format_version(version_dict, revisionSep=":"):
    ret = version_dict['MAJOR'] + "." + version_dict['MINOR'] + "." + version_dict['PATCH']
    if int(version_dict['REVISION']) > 0:
        ret = version_dict['REVISION'] + revisionSep + ret
    if version_dict['BUILD'] != "0":
        ret = ret + "-" + version_dict['BUILD']
    return ret

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manages the version change in a .env file.')
    parser.add_argument('-e', '--env-path', type=str, default='./.env',
                        action="store", help='.env file path')
    parser.add_argument('-p', metavar='package', type=str,
                        help='Package name definition')
    parser.add_argument('-a', metavar='architecture', type=str,
                        help='Architecture definition')
    advance = parser.add_argument_group("Version increase options")
    advance.add_argument('--next', action="store_true",
                        help='Increase minor version')
    advance.add_argument('--next-revision', action="store_true",
                        help='Increase revision version')
    parser.add_argument('-w', '--write', action="store_true",
                        help='Writes the change in the .env file')
    git = parser.add_argument_group("Git management options")
    git.add_argument('-c', '--commit', action="store_true",
                        help='Commits changes into git repository')
    git.add_argument('-u', '--user-email', action="store", nargs=2, metavar=("USER", "EMAIL"),
                        help='Git user and email configuration')
    git.add_argument('--private-key', action="store", nargs=1,
                        help='SSH private key')
    git.add_argument('--private-key-dir', action="store", nargs=1, type=str, default='/root/.ssh',
                        help='SSH private key')
    showg = parser.add_argument_group("Output one value")
    show = showg.add_mutually_exclusive_group()
    show.add_argument('--minor', action="store_true",
                        help='Shows minor version')
    show.add_argument('--major', action="store_true",
                        help='Shows major version')
    show.add_argument('--patch', action="store_true",
                        help='Shows patch version')
    show.add_argument('--revision', action="store_true",
                        help='Shows revision version')
    show.add_argument('--build', action="store_true",
                        help='Shows build version')
    args = parser.parse_args(sys.argv[1:])

    # Env file reading
    with open(args.env_path) as f:
        lines = f.readlines()

    # Fields extraction
    version_dict={}
    rest_of_the_env=[]
    for line in lines:
        found = versions.findall(line)
        if len(found) > 0:
            version_dict[found[0][0]]=found[0][1]
        else:
            rest_of_the_env.append(line)

    # Build ID environment value
    buildId = os.getenv('PROJECT_VERSION_BUILD')
    if buildId is not None:
        version_dict['BUILD'] = buildId

    # Fields checking
    if not all(k in version_dict for k in ('MAJOR', 'MINOR', 'PATCH', 'REVISION', 'BUILD')):
        print("Bad env file", file=sys.stderr)
        sys.exit(1)
    orig_version_dict = version_dict.copy()

    # Increase options
    if args.next:               version_dict['PATCH'] = str(int(version_dict['PATCH']) + 1)
    if args.next_revision:      version_dict['REVISION'] = str(int(version_dict['REVISION']) + 1)

    # Version prompt
    if args.major:      print(version_dict['MAJOR'])
    elif args.minor:    print(version_dict['MINOR'])
    elif args.patch:    print(version_dict['PATCH'])
    elif args.revision: print(version_dict['REVISION'])
    elif args.build: print(version_dict['BUILD'])
    else:
        version_str = [args.p, format_version(version_dict), args.a]
        print('_'.join(filter(None, version_str)))

    if args.write:
        # Content generation
        new_content=""
        for c,v in version_dict.items():
            if c != 'BUILD':
                new_content+='PROJECT_VERSION_' + c + '=' + v + '\n'
            else:
                new_content+='PROJECT_VERSION_BUILD=0 # Filled out by CI\n'

        # File writing
        with open(args.env_path, 'w') as f:
            f.write(new_content)
            f.write(''.join(rest_of_the_env))

    if args.commit:
        # Private key management
        if args.private_key:
            subprocess.call(["mkdir", "-p", args.private_key_dir])
            with open(args.private_key_dir + "/id_rsa", 'w') as k:
                k.write(args.private_key[0] + "\n")
            subprocess.call(["chmod", "600", args.private_key_dir + "/id_rsa"])
            subprocess.call(["chown", "root:root", args.private_key_dir + "/id_rsa"])

        # Git user and email management
        if args.user_email \
            and (subprocess.call(["git", "config", "user.name", args.user_email[0]]) != 0 \
            or subprocess.call(["git", "config", "user.email", args.user_email[1]]) != 0):
                raise RuntimeError("Failed to set git config")

        # Commit and tag management
        commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf8").replace("\n", "")
        tag_messagge = subprocess.check_output(["git", "log", "--format=%B", "-n", "1", commit_hash]).decode("utf8").replace("\n", "")
        if subprocess.call(["git", "tag", "-a", format_version(orig_version_dict, revisionSep="r"), "-m", tag_messagge]) != 0 \
            or subprocess.call(["git", "add", args.env_path]) != 0 \
            or subprocess.call(["git", "commit", "-m", "[skip ci] Increase version to " + format_version(version_dict)]) != 0 \
            or subprocess.call(["git", "push"]) != 0 \
            or subprocess.call(["git", "push", "--tags"]) != 0:
                raise RuntimeError("Failed to commit and tag new version")
