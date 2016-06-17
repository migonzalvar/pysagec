import logging
from urllib.request import Request, urlopen

from .renderers import XMLRenderer
from .parsers import XMLParser

logger = logging.getLogger(__name__)


def soap(tag):
    return '{http://www.w3.org/2003/05/soap-envelope}%s' % tag


def mrw(tag):
    return '{http://www.mrw.es/}%s' % tag


class Client:
    def __init__(self, hostname, auth_info):
        self.base_url = 'http://{}/MRWEnvio.asmx'.format(hostname)
        self.auth_info = auth_info
        self.parser = XMLParser()
        self.renderer = XMLRenderer()

    def make_http_request(self, tag, request_data, extra_headers=None):
        # TODO: insert header 'SOAPAction: "http://www.mrw.es/GetEtiquetaEnvio"
        extra_headers = extra_headers or {}
        data = [
            {'soap:Header': self.auth_info.as_dict()},
            {'soap:Body': {
                tag: {
                    'mrw:request': request_data
                },
            }},
        ]
        namespaces = [
            ('soap', 'http://www.w3.org/2003/05/soap-envelope'),
            ('mrw', 'http://www.mrw.es/'),
        ]
        data = self.renderer.render({'soap:Envelope': data}, namespaces)
        logger.debug('Sending %s', data)
        headers = {'Content-type': 'application/soap+xml; charset=utf-8'}
        headers.update(extra_headers)
        return Request(self.base_url, data, headers, method='POST')

    def send(self, pickup_info, service_info):
        request_data = [pickup_info.as_dict(), service_info.as_dict()]
        req = self.make_http_request('mrw:TransmEnvio', request_data)
        with urlopen(req) as response:
            body = response.read()
            logger.debug('Received %s', body)

        response = self.parser.parse(body)

        # WIP: move to a model Model

        shipping_number = (
            response[soap('Envelope')][0]
            [soap('Body')][0]
            [mrw('TransmEnvioResponse')][0]
            [mrw('TransmEnvioResult')][3]
            [mrw('NumeroEnvio')]
        )

        return {'shipping_number': shipping_number}

    def get_label(self, get_label_request):
        request_data = [get_label_request.as_dict()[None]]
        req = self.make_http_request('mrw:GetEtiquetaEnvio', request_data)
        with urlopen(req) as response:
            body = response.read()
            logger.debug('Received %s', body)

        response = self.parser.parse(body)
        pdf = (
            response[soap('Envelope')][0]
            [soap('Body')][0]
            [mrw('GetEtiquetaEnvioResponse')][0]
            [mrw('GetEtiquetaEnvioResult')][2]
            [mrw('EtiquetaFile')]
        )
        return {'file': pdf}
