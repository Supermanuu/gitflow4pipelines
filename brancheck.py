#!/usr/bin/env python3

import sys
import argparse

development = 'refs/heads/development'
integration = 'refs/heads/integration'
main = 'refs/heads/main'

feature = 'refs/heads/feature/'
bug = 'refs/heads/bug/'
fix = 'refs/heads/fix/'
hotfix = 'refs/heads/hotfix/'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Checks SEDECAL\'s git flow.')
    parser.add_argument('source', type=str, help='PR source branch')
    parser.add_argument('target', type=str, help='PR destination branch')
    args = parser.parse_args(sys.argv[1:])

    # On PR the source branch is the branch which is going to be merged and the 
    # target branch is the branch where the merge is going to be performed
    #   feature/*, bug/*, integration -> development
    #   fix/*, development, main -> integration
    #   hotfix/*, integration -> main

    print(f"Checking PR from '{args.source}' to '{args.target}'")

    good=False
    if args.target == development:
        good = args.source.startswith(feature) or args.source.startswith(bug)
    elif args.target == integration:
        good = args.source.startswith(fix) or args.source == development
    elif args.target == main:
        good = args.source.startswith(hotfix) or args.source == integration
    else:
        raise RuntimeError("Bad target branch", file=sys.stderr)
    if not good:
        raise RuntimeError(f"Cannot merge from '{args.source}' to '{args.target}'", file=sys.stderr)
