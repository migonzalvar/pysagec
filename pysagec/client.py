from urllib.request import Request, urlopen


STUB = b'''
<soap:Envelope
  xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
  xmlns:mrw="http://www.mrw.es/">
<soap:Header>
<mrw:AuthInfo>
<mrw:CodigoFranquicia>String</mrw:CodigoFranquicia>
<mrw:CodigoAbonado>String</mrw:CodigoAbonado>
<mrw:CodigoDepartamento>String</mrw:CodigoDepartamento>
<mrw:UserName>String</mrw:UserName>
<mrw:Password>String</mrw:Password>
</mrw:AuthInfo>
</soap:Header>
<soap:Body>
<mrw:TransmEnvio>
</mrw:TransmEnvio>
</soap:Body>
</soap:Envelope>
'''


class Client:
    def __init__(self, hostname='sagec-test.mrw.es'):
        self.base_url = 'http://{}/MRWEnvio.asmx'.format(hostname)

    def make_http_request(self):
        data = STUB
        headers = {'Content-type': 'application/soap+xml; charset=utf-8'}
        return Request(self.base_url, data, headers, method='POST')

    def send(self):
        req = self.make_http_request()
        with urlopen(req) as response:
            body = response.read()
            body = body.decode('utf-8')
            return body
