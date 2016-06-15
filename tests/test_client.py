from unittest.mock import patch

from pysagec import Client


class MockModel:
    def as_dict(self):
        return {}


def test_client_init():
    client = Client('example.com', MockModel())
    assert client.base_url == 'http://example.com/MRWEnvio.asmx'


def test_client_make_http_request():
    client = Client('example.com', MockModel())
    req = client.make_http_request(MockModel(), MockModel())
    assert req.get_method() == 'POST'


def test_send_with_mock():
    with patch('pysagec.client.urlopen') as urlopen:
        client = Client('example.com', MockModel())
        client.send(MockModel(), MockModel())
    assert urlopen.called
