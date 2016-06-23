import base64
from urllib.parse import urlsplit


def base64_to_file(data, filename):
    data = base64.b64decode(data)
    with open(filename, 'wb') as fp:
        fp.write(data)


def get_hostname_from_url(url):
    url = urlsplit(url)
    return url.hostname
