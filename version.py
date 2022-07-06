#!/usr/bin/env python3

import os
import re
import sys
import argparse

versions = re.compile(r'^PROJECT_VERSION_([^=]+)=(\d+)$')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manages the version change in a .env file.')
    parser.add_argument('-e', '--env-path', type=str, default='./.env',
                        action="store", help='.env file path')
    parser.add_argument('-p', metavar='package', type=str,
                        help='Package name definition')
    parser.add_argument('-a', metavar='architecture', type=str,
                        help='Architecture definition')
    parser.add_argument('--next', action="store_true",
                        help='Increase minor version')
    parser.add_argument('--next-fix', action="store_true",
                        help='Increase major version')
    parser.add_argument('--next-hotfix', action="store_true",
                        help='Increase patch version')
    parser.add_argument('-w', '--write', action="store_true",
                        help='Writes the change in the .env file')
    show = parser.add_mutually_exclusive_group()
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
        version_str = [args.p, str(version_dict['MAJOR'] + "." +
            version_dict['MINOR'] + "." +
            version_dict['PATCH'] +
            ("f" + version_dict['FIX'] if int(version_dict['FIX']) > 0 else "") +
            ("h" + version_dict['HOTFIX'] if int(version_dict['HOTFIX']) > 0 else "")), args.a]
        print('_'.join(filter(None, version_str)))

    new_content=""
    for c,v in version_dict.items():
        new_content+='PROJECT_VERSION_' + c + '=' + v + '\n'
    if args.write:
        with open(args.env_path, 'w') as f:
            f.write(new_content)
            f.write(''.join(rest_of_the_env))
