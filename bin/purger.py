import json
import socket
import subprocess
import urllib

try:
    from urllib.parse import urlparse
except ImportError:
    # py2
    from urlparse import urlparse

import settings

def create_purge_command(url, cmd_template):
    parsed = urlparse(url)
    delete_cmd = None

    if parsed.netloc:
        delete_cmd = cmd_template.format(path=parsed.path)

    return delete_cmd

def purge(hostname):

    get_url = '{url}/hosts/pending_purge?hostname={hostname}'.format(
        url=settings.API_URL, hostname=hostname)

    notify_url = '{url}/purge'.format(url=settings.API_URL)

    response = urllib.urlopen(get_url)
    urls = json.loads(response.read())

    for url in urls:
        purge_cmd = create_purge_command(url, settings.DELETE_TMPLT)

        if purge_cmd:
            # execute delete
            cmd_output = subprocess.check_output(purge_cmd, shell=True)

            params = urllib.urlencode({
                'url': url,
                'hostname': hostname,
                'command_output': cmd_output
            })

            _ = urllib.urlopen(notify_url, params)

if __name__ == '__main__':
    purge(socket.gethostname())
