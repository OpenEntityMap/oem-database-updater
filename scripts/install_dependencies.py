from argparse import ArgumentParser
from subprocess import Popen
import os


DEPENDENCIES = [
    ('flake8', [
        'flake8==2.6.0'
    ]),
    ('py32', [
        'coverage==3.7.1'
    ]),
    ('develop', [
        '-rrequirements_develop.txt',
        '-rtests/requirements_develop.txt'
    ]),
    ('pip', [
        '-rrequirements.txt',
        '-rtests/requirements.txt'
    ]),
    ('travis', [
        '-rrequirements_vendor.txt',
        '-rtests/requirements_vendor.txt',

        '--editable=git://github.com/fuzeman/bencode.py.git#egg=bencode.py',

        '--editable=git+https://github.com/OpenEntityMap/oem-framework.git@{BRANCH}#egg=oem-framework',
        '--editable=git+https://github.com/OpenEntityMap/oem-core.git@{BRANCH}#egg=oem-core'
    ])
]


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('env')

    args = parser.parse_args()

    # Retrieve branch
    branch = os.environ.get('CURRENT_BRANCH') or 'master'

    # Install environment dependencies
    env_parts = args.env.split('-')

    for key, dependencies in DEPENDENCIES:
        if key not in env_parts:
            continue

        for dep in dependencies:
            dep = dep.replace('{BRANCH}', branch)

            # Install dependency
            print('Installing dependency: %r' % (dep,))
            process = Popen(['pip', 'install', dep])
            process.wait()
