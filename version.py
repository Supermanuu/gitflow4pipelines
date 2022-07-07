#!/usr/bin/env python3

import re
import sys
import argparse
import subprocess

versions = re.compile(r'^PROJECT_VERSION_([^=]+)=(\d+)$')

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
    advance.add_argument('--next-fix', action="store_true",
                        help='Increase major version')
    advance.add_argument('--next-hotfix', action="store_true",
                        help='Increase patch version')
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
    show.add_argument('--fix', action="store_true",
                        help='Shows fix version')
    show.add_argument('--hotfix', action="store_true",
                        help='Shows hotfix version')
    args = parser.parse_args(sys.argv[1:])

    with open(args.env_path) as f:
        lines = f.readlines()

    version_dict={}
    rest_of_the_env=[]
    for line in lines:
        found = versions.findall(line)
        if len(found) > 0:
            version_dict[found[0][0]]=found[0][1]
        else:
            rest_of_the_env.append(line)
    if not all(k in version_dict for k in ('MAJOR', 'MINOR', 'PATCH', 'FIX', 'HOTFIX')):
        print("Bad env file", file=sys.stderr)
        sys.exit(1)

    if args.next:           version_dict['PATCH'] = str(int(version_dict['PATCH']) + 1)
    if args.next_fix:       version_dict['FIX'] = str(int(version_dict['FIX']) + 1)
    if args.next_hotfix:    version_dict['HOTFIX'] = str(int(version_dict['HOTFIX']) + 1)

    if args.major:      print(version_dict['MAJOR'])
    elif args.minor:    print(version_dict['MINOR'])
    elif args.patch:    print(version_dict['PATCH'])
    elif args.fix:      print(version_dict['FIX'])
    elif args.hotfix:   print(version_dict['HOTFIX'])
    else:
        major_minor_patch = version_dict['MAJOR'] + "." \
            + version_dict['MINOR'] + "." \
            + version_dict['PATCH']
        version_str = [args.p, str(major_minor_patch
            + ("f" + version_dict['FIX'] if int(version_dict['FIX']) > 0 else "")
            + ("h" + version_dict['HOTFIX'] if int(version_dict['HOTFIX']) > 0 else "")), args.a]
        print('_'.join(filter(None, version_str)))

    new_content=""
    for c,v in version_dict.items():
        new_content+='PROJECT_VERSION_' + c + '=' + v + '\n'
    if args.write:
        with open(args.env_path, 'w') as f:
            f.write(new_content)
            f.write(''.join(rest_of_the_env))
        if args.private_key:
            subprocess.call(["mkdir", "-p", args.private_key_dir])
            with open(args.private_key_dir + "/id_rsa", 'w') as k:
                k.write(args.private_key[0] + "\n")
            subprocess.call(["chmod", "600", args.private_key_dir + "/id_rsa"])
            subprocess.call(["chown", "root:root", args.private_key_dir + "/id_rsa"])
        if args.user_email \
            and (subprocess.call(["git", "config", "user.name", args.user_email[0]]) != 0 \
            or subprocess.call(["git", "config", "user.email", args.user_email[1]]) != 0):
                raise RuntimeError("Failed to set git config")
        if args.commit:
            commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf8").replace("\n", "")
            tag_messagge = subprocess.check_output(["git", "log", "--format=%B", "-n", "1", commit_hash]).decode("utf8").replace("\n", "")
            if subprocess.call(["git", "add", args.env_path]) != 0 \
            or subprocess.call(["git", "commit", "-m", "[skip ci] Generating new version " + major_minor_patch]) != 0 \
            or subprocess.call(["git", "tag", "-a", major_minor_patch, "-m", tag_messagge]) != 0 \
            or subprocess.call(["git", "push"]) != 0 \
            or subprocess.call(["git", "push", "--tags"]) != 0:
                raise RuntimeError("Failed to commit and tag new version")
