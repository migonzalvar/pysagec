import logging
from urllib.request import Request, urlopen

from .renderers import XMLRenderer


logger = logging.getLogger('pysagec')


class Client:
    def __init__(self, hostname, auth_info):
        self.base_url = 'http://{}/MRWEnvio.asmx'.format(hostname)
        self.auth_info = auth_info
        self.renderer = XMLRenderer()

    def make_http_request(self, pickup_info, service_info):
        data = [
            {'soap:Header': self.auth_info.as_dict()},
            {'soap:Body': {
                'mrw:TransmEnvio': {
                    'mrw:request': [
                        pickup_info.as_dict(),
                        service_info.as_dict(),
                    ]
                },
            }},
        ]
        namespaces = [
            ('soap', 'http://www.w3.org/2003/05/soap-envelope'),
            ('mrw', 'http://www.mrw.es/'),
        ]
        data = self.renderer.render({'soap:Envelope': data}, namespaces)

        headers = {'Content-type': 'application/soap+xml; charset=utf-8'}
        return Request(self.base_url, data, headers, method='POST')

    def send(self, pickup_info, service_info):
        req = self.make_http_request(pickup_info, service_info)
        with urlopen(req) as response:
            body = response.read()
            body = body.decode('utf-8')
            return body
