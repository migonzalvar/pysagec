from pysagec import models
from pysagec.renderers import XMLRenderer


def test_main():
    data = {
        'soap:Header': models.AuthInfo().as_dict(),
        'soap:Body': {
            'mrw:TransmEnvio': {
                'mrw:request': [
                    models.PickupInfo().as_dict(),
                    models.ServiceInfo().as_dict(),
                ]
            }
        }
    }
    namespaces = [
        ('soap', 'http://www.w3.org/2003/05/soap-envelope'),
        ('mrw', 'http://www.mrw.es/'),
    ]
    xml = XMLRenderer().render({'soap:Envelope': data}, namespaces)
    assert isinstance(xml, bytes)
