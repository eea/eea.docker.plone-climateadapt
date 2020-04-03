#!/usr/bin/env python2

import shutil
import subprocess
import json
import os
from decimal import Decimal
from urlparse import urlparse


def run_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    (response, err) = p.communicate()
    p_status = p.wait()
    return (response, err)


def _tag_release(version):
    if os.path.isfile('./token'):
        with open('./token') as f:
            read_data = f.read()
        token = read_data.strip()
    else:
        print "Could not make release: token not found"
        return

    payload = {
        "target_commitish": "master",
        'tag_name': 'v' + str(version),
        'name': 'v' + str(version),
        'body': 'Release ' + str(version),
    }

    (url, err) = run_command(['git', 'config', '--get', 'remote.origin.url'])
    data = urlparse(url)
    path = data.path.replace('.git', '')
    url = 'https://api.github.com/repos' + path.strip() + '/releases'
    (resp, err) = run_command(['curl', '-H', 'Authorization: token '+str(token), url, '-X', 'POST', '-d', json.dumps(payload) ])
    data = json.loads(resp)
    if 'message' in data:
        print "Release error:" + data['message']


def release():
    with open('buildout.cfg', 'r') as f:
        lines = f.read().split('\n')

    out = []

    found = False

    for line in lines:
        if (not found) and line.startswith('# v'):
            line = line.replace('# v', '')
            left, right = line.split(' ', 1)
            digits = left.strip()
            version = Decimal(digits)
            version += Decimal('0.01')
            line = '# v{} {}'.format(version, right).strip()
            found = True

        out.append(line)

    shutil.copyfile('buildout.cfg', 'buildout.cfg.old')
    with open('buildout.cfg', 'w') as f:
        f.write('\n'.join(out))

    subprocess.call(['git', 'pull'])
    subprocess.call(['git', 'commit', 'buildout.cfg', '-m', '"Bump version"'])
    subprocess.call(['git', 'tag', '-a', "v{}".format(version), '-m',
                     'Release {}'.format(version)])
    subprocess.call(['git', 'push', '--tags'])
    subprocess.call(['git', 'push'])

    _tag_release(version)


if __name__ == "__main__":
    release()
