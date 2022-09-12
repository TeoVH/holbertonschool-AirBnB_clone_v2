#!/usr/bin/python3
"""
Script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo
"""
from datetime import datetime
from os.path import isdir
from fabric.api import local


def do_pack():
    """Generates a .tgz archive"""
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(date)
    try:
        if isdir("versions") is False:
            local("mkdir versions")
        local("tar -cvzf {} web_static".format(file))
        return file
    except Exception:
        return None
