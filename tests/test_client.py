import os
from urllib.parse import urlsplit, parse_qs

import pytest

from pysagec import Client
from pysagec.models import AuthInfo, PickupInfo, ServiceInfo


def key_or_none(qs, key):
    iterable = qs.get(key, [None])
    return iterable[0]


class MockModel:
    def as_dict(self):
        return {}


@pytest.fixture
def test_client():
    import logging
    logging.basicConfig(level=logging.DEBUG)

    url = os.environ.get(
        'TEST_URL',
        '//user:pass@example.com/?franchise=12&subscriber=34&department=56'
    )

    url = urlsplit(url)
    qs = parse_qs(url.query)

    hostname = url.hostname
    kwargs = {
        'username': url.username,
        'franchise_code': key_or_none(qs, 'franchise'),
        'subscriber_code': key_or_none(qs, 'subscriber'),
        'departament_code': key_or_none(qs, 'department'),
    }
    auth_info = AuthInfo(**kwargs)
    return Client(hostname, auth_info)


def test_client_init():
    client = Client('example.com', MockModel())
    assert client.base_url == 'http://example.com/MRWEnvio.asmx'


def test_client_make_http_request():
    client = Client('example.com', MockModel())
    req = client.make_http_request(MockModel(), MockModel())
    assert req.get_method() == 'POST'


@pytest.mark.skipif(
    not os.environ.get('TEST_URL', False),
    reason='TEST_URL environment is no set',
)
def test_send(test_client):
    pickup_info = PickupInfo()
    service_info = ServiceInfo()
    body = test_client.send(pickup_info, service_info)
    print(body)
