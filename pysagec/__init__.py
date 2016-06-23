from .client import Client
from .models import AuthInfo
from .utils import get_hostname_from_url


__all__ = ['Client', 'create_client']


def create_client(url):
    hostname = get_hostname_from_url(url)
    auth_info = AuthInfo.from_url(url)
    return Client(hostname, auth_info)
