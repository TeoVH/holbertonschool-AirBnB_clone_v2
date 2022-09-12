#!/usr/bin/python3
"""
Script that distributes an archive to your web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['3.208.25.96', '3.89.66.142']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not exists(archive_path):
        return False
    try:
        file = archive_path.split('/')[-1].split('.')[0]
        put(archive_path, "/tmp/")
        run('mkdir -p /data/web_static/releases/{}/'.format(file))
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}'
            .format(file, file))
        run('rm /tmp/{}.tgz'.format(file))
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}'.format(file, file))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(file))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}\
            /data/web_static/current'.format(file))
        return True
    except Exception as e:
        return False
