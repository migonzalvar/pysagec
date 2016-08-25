from contextlib import contextmanager
from unittest.mock import patch, MagicMock

from pysagec import Client


class MockModel:
    def as_dict(self):
        return {}


class MockLabelRequest:
    def as_dict(self):
        return {None: []}


@contextmanager
def patched_client(body_response):
    with patch('pysagec.client.urlopen', read=b'a') as urlopen_:
        response = urlopen_.return_value.__enter__.return_value
        response.read.return_value = body_response
        client = Client('example.com', MockModel())
        get_label_request = MagicMock()
        get_label_request.as_dict.return_value = {None: []}
        yield client

    assert urlopen_.called


def test_client_init():
    client = Client('example.com', MockModel())
    assert client.base_url == 'http://example.com/MRWEnvio.asmx'


def test_client_make_http_request():
    client = Client('example.com', MockModel())
    req = client.make_http_request('tag', {})
    assert req.get_method() == 'POST'


def test_send_with_mock():
    body_response = (
        b'<?xml version="1.0" encoding="utf-8"?>'
        b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"'
        b' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        b' xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
        b'<soap:Body>'
        b'<TransmEnvioResponse xmlns="http://www.mrw.es/">'
        b'<TransmEnvioResult>'
        b'<Estado>1</Estado>'
        b'<Mensaje>1) La fecha de recogida solicitada es 01/08/2016.</Mensaje>'
        b'<NumeroSolicitud>0330550767020160615223238261</NumeroSolicitud>'
        b'<NumeroEnvio>033050000050</NumeroEnvio>'
        b'<Url>http://sagec-test.mrw.es/Panel.aspx</Url>'
        b'</TransmEnvioResult>'
        b'</TransmEnvioResponse>'
        b'</soap:Body>'
        b'</soap:Envelope>'
    )
    with patched_client(body_response) as client:
        response = client.send(MockModel(), MockModel())
    assert '1' == response.status
    assert '033050000050' == response.shipping_number


def test_get_label_with_mock():
    body_response = (
        b'<?xml version="1.0" encoding="utf-8"?>'
        b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"'
        b' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        b' xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
        b'<soap:Body>'
        b'<GetEtiquetaEnvioResponse xmlns="http://www.mrw.es/">'
        b'<GetEtiquetaEnvioResult>'
        b'<Estado>1</Estado>'
        b'<Mensaje/>'
        b'<EtiquetaFile>AA==</EtiquetaFile>'
        b'</GetEtiquetaEnvioResult>'
        b'</GetEtiquetaEnvioResponse>'
        b'</soap:Body>'
        b'</soap:Envelope>'
    )
    with patched_client(body_response) as client:
        response = client.get_label(MockLabelRequest())
    assert '1' == response.status
    assert 'AA==' == response.file


def test_get_label_with_error_with_mock():
    body_response = (
        b'<?xml version="1.0" encoding="utf-8"?>'
        b'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope"'
        b' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'
        b' xmlns:xsd="http://www.w3.org/2001/XMLSchema">'
        b'<soap:Body>'
        b'<GetEtiquetaEnvioResponse xmlns="http://www.mrw.es/">'
        b'<GetEtiquetaEnvioResult>'
        b'<Estado>0</Estado>'
        b'<Mensaje/>'
        b'</GetEtiquetaEnvioResult>'
        b'</GetEtiquetaEnvioResponse>'
        b'</soap:Body>'
        b'</soap:Envelope>'
    )
    with patched_client(body_response) as client:
        response = client.get_label(MockLabelRequest())
    assert '0' == response.status
