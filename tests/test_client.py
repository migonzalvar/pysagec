import os
import pytest

from pysagec import Client
from pysagec.models import AuthInfo, PickupInfo, ServiceInfo


class MockModel:
    def as_dict(self):
        return {}


@pytest.fixture
def test_client():
    return Client('sagec-test.mrw.es', AuthInfo())


def test_client_init():
    client = Client('example.com', MockModel())
    assert client.base_url == 'http://example.com/MRWEnvio.asmx'


def test_client_make_http_request():
    client = Client('example.com', MockModel())
    req = client.make_http_request(MockModel(), MockModel())
    assert req.get_method() == 'POST'


@pytest.mark.skipif(
    os.environ.get('TEST_PRE') != 'true',
    reason='TEST_PRE=true is no set',
)
def test_send(test_client):
    pickup_info = PickupInfo()
    service_info = ServiceInfo()
    body = test_client.send(pickup_info, service_info)
    print(body)
