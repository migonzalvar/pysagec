import os
import pytest

from pysagec import Client


@pytest.fixture
def client():
    return Client()


def test_client_init():
    sagec = Client('example.com')
    assert sagec.base_url == 'http://example.com/MRWEnvio.asmx'


def test_client_make_http_request(client):
    req = client.make_http_request()
    assert req.get_method() == 'POST'


@pytest.mark.skipif(
    os.environ.get('TEST_PRE') != 'true',
    reason='TEST_PRE=true is no set',
)
def test_send(client):
    body = client.send()
    print(body)
