import os
import subprocess
import sys

from pysagec import create_client
from pysagec import models
from pysagec import utils

import pytest


def launch(filename):
    if sys.platform == "win32":
        os.startfile(filename)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filename])


@pytest.fixture
def pre_production_client():
    import logging
    logging.basicConfig(level=logging.DEBUG)

    url = os.environ.get(
        'TEST_URL',
        '//user:pass@example.com/?franchise=12&subscriber=34&department=56'
    )
    return create_client(url)


@pytest.mark.skipif(
    not os.environ.get('TEST_URL', False),
    reason='TEST_URL environment is no set',
)
def test_send(pre_production_client):
    address = models.Address()
    address.street_name = 'Plaza de España'
    address.postal_code = '36001'
    address.city = 'Pontevedra'
    pickup_info = models.PickupInfo()
    pickup_info.pickup_address = address
    pickup_info.recipient_name = 'Juan Pérez'
    service_info = models.ServiceInfo()
    service_info.number_of_packages = 1
    service_info.date = '01/08/2016'
    service_info.service_code = '0000'

    response = pre_production_client.send(pickup_info, service_info)
    print(repr(response))
    assert isinstance(response, dict)
    assert 'shipping_number' in response

    get_label = models.GetLabel()
    get_label.shipping_number = response['shipping_number']

    response = pre_production_client.get_label(get_label)
    print(repr(response))
    assert isinstance(response, dict)
    assert 'file' in response

    utils.base64_to_file(response['file'], 'label.pdf')
    launch('label.pdf')
