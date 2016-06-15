import os
from urllib.parse import urlsplit, parse_qs

from pysagec import Client
from pysagec.models import AuthInfo, Address, PickupInfo, ServiceInfo

import pytest


def key_or_none(qs, key):
    iterable = qs.get(key, [None])
    return iterable[0]


@pytest.fixture
def pre_production_client():
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
        'password': url.password,
        'franchise_code': key_or_none(qs, 'franchise'),
        'subscriber_code': key_or_none(qs, 'subscriber'),
        'departament_code': key_or_none(qs, 'department'),
    }
    auth_info = AuthInfo(**kwargs)
    return Client(hostname, auth_info)


@pytest.mark.skipif(
    not os.environ.get('TEST_URL', False),
    reason='TEST_URL environment is no set',
)
def test_send(pre_production_client):
    address = Address()
    address.street_name = 'Plaza de España'
    address.postal_code = '36001'
    address.city = 'Pontevedra'
    pickup_info = PickupInfo()
    pickup_info.pickup_address = address
    pickup_info.recipient_name = 'Juan Pérez'
    service_info = ServiceInfo()
    service_info.number_of_packages = 1
    service_info.date = '01/08/2016'
    service_info.service_code = '0000'

    body = pre_production_client.send(pickup_info, service_info)
    assert isinstance(body, str)