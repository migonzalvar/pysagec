import logging
from urllib.request import Request, urlopen

from .renderers import XMLRenderer
from .parsers import XMLParser

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, hostname, auth_info):
        self.base_url = 'http://{}/MRWEnvio.asmx'.format(hostname)
        self.auth_info = auth_info
        self.parser = XMLParser()
        self.renderer = XMLRenderer()

    def make_http_request(self, tag='mrw:TransmEnvio', models_=None, extra_headers=None):
        models_ = models_ or []
        extra_headers = extra_headers or {}
        data = [
            {'soap:Header': self.auth_info.as_dict()},
            {'soap:Body': {
                tag: {
                    'mrw:request': [model.as_dict() for model in models_]
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
        models_ = [pickup_info, service_info]
        req = self.make_http_request('mrw:TransmEnvio', models_)
        with urlopen(req) as response:
            body = response.read()
            logger.debug('Received %s', body)

        response = self.parser.parse(body)

        # WIP: move to a model Model

        def soap(tag):
            return '{http://www.w3.org/2003/05/soap-envelope}%s' % tag

        def mrw(tag):
            return '{http://www.mrw.es/}%s' % tag

        shipping_number = (
            response[soap('Envelope')][0]
            [soap('Body')][0]
            [mrw('TransmEnvioResponse')][0]
            [mrw('TransmEnvioResult')][3]
            [mrw('NumeroEnvio')]
        )

        return {'shipping_number': shipping_number}
