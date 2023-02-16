#!/usr/bin/env python

main = 'main'
master = 'master'
release = 'release/'
integration = 'integration'

bug = 'bug/'
fix = 'fix/'
bugfix = 'bugfix/'
hotfix = 'hotfix/'
feature = 'feature/'

def brancheck(rawSource, rawTarget):
    source = rawSource.replace('refs/heads/', '')
    target = rawTarget.replace('refs/heads/', '')

    good=False
    if release in target:
        good = source.startswith(release) or source.startswith(feature) or source.startswith(bug) or source.startswith(bugfix)
    elif target == integration:
        good = source.startswith(fix) or source.startswith(release)
    elif target == main or target == master:
        good = source.startswith(hotfix) or source == integration
    else:
        raise RuntimeError('Bad target branch')
    if not good:
        raise RuntimeError('Cannot merge from ' + source + ' to ' + target)


if __name__ == '__main__':
    import sys
    if sys.version_info[0] == 2:
        from dotdict import Dotdict
        if len(sys.argv) == 3:
            args = Dotdict({
                'source'     : sys.argv[1],
                'target'     : sys.argv[2]
            })
        else:
            print('Usage: ' + sys.argv[0] + ' <source> <target>')
            exit(2)
    else:
        import argparse
        parser = argparse.ArgumentParser(description='Checks SEDECAL\'s git flow.')
        parser.add_argument('source', type=str, help='PR source branch')
        parser.add_argument('target', type=str, help='PR destination branch')
        args = parser.parse_args(sys.argv[1:])

    # On PR the source branch is the branch which is going to be merged and the 
    # target branch is the branch where the merge is going to be performed
    #   feature/*, bug/*, integration -> development
    #   fix/*, development, main -> integration
    #   hotfix/*, integration -> main

    print('Checking PR from ' + args.source + ' to '  + args.target)

    brancheck(args.source, args.target)
