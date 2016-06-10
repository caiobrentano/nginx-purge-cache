import json
import socket
import urllib

from urllib.parse import urlparse

import settings

def create_purge_command(url, cmd_template):
    parsed = urlparse(url)

    if parsed.netloc:
        delete_cmd = cmd_template.format(path=parsed.path)

    return delete_cmd

def purge(hostname, url):

    response = urllib.urlopen(url)
    urls = json.loads(response.read())

    for url in urls:
        purge_cmd = create_purge_command(url, settings.DELETE_TMPLT)

        if purge_cmd:
            pass
            # execute delete
            # cmd_output = subprocess.check_output(purge_cmd, shell=True)

if __name__ == 'main':
    hostname = socket.gethostname()

    url = '{url}/hosts/pending_purge?hostname={hostname}'.format(
        url=settings.API_URL, hostname=hostname)

    purge(hostname, url)
