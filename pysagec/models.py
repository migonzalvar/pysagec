from urllib.parse import urlsplit, parse_qs

from .base import Model, Nested, String


def key_or_none(qs, key):
    iterable = qs.get(key, [None])
    return iterable[0]


class AuthInfo(Model):
    root_tag = 'mrw:AuthInfo'

    franchise_code = String('mrw:CodigoFranquicia')
    subscriber_code = String('mrw:CodigoAbonado')
    departament_code = String('mrw:CodigoDepartamento', ignore_if_none=True)
    username = String('mrw:UserName')
    password = String('mrw:Password')

    @classmethod
    def from_url(cls, url):
        url = urlsplit(url)
        qs = parse_qs(url.query)
        return cls(
            username=url.username,
            password=url.password,
            franchise_code=key_or_none(qs, 'franchise'),
            subscriber_code=key_or_none(qs, 'subscriber'),
            departament_code=key_or_none(qs, 'department')
        )


class Address(Model):
    root_tag = 'mrw:Direccion'

    street_type = String('mrw:CodigoTipoVia')
    street_name = String('mrw:Via')
    street_number = String('mrw:Numero')
    remaining_details = String('mrw:Resto')
    postal_code = String('mrw:CodigoPostal')
    city = String('mrw:Poblacion')


class PickupInfo(Model):
    root_tag = 'mrw:DatosEntrega'

    pickup_address = Nested('mrw:Direccion', Address, unwrap=True)
    vat_number = String('mrw:Nif')
    recipient_name = String('mrw:Nombre')
    recipient_phone_number = String('mrw:Telefono')
    contact_phone_number = String('mrw:Contacto')
    contact_name = String('mrw:ALaAtencionDe')
    comments = String('mrw:Observaciones')


class Package(Model):
    root_tag = 'mrw:BultoRequest'

    height = String('mrw:Alto')
    length = String('mrw:Largo')
    width = String('mrw:Ancho')
    dimension = String('mrw:Dimension')
    reference = String('mrw:Referencia')
    weight = String('mrw:Peso')


class ServiceInfo(Model):
    root_tag = 'mrw:DatosServicio'

    date = String('mrw:Fecha')
    customer_reference = String('mrw:Referencia')
    franchise_delivery = String('mrw:EnFranquicia', default='N')
    service_code = String('mrw:CodigoServicio')
    packages = Nested('mrw:Bultos', Package, many=True)
    number_of_packages = String('mrw:NumeroBultos')
    weight = String('mrw:Peso')
    delivery_on_saturday = String('mrw:EntregaSabado', default='N')
    delivery_before_830 = String('mrw:Entrega830', default='N')
    delivery_after_time = String('mrw:EntregaPartirDe')
    management = String('mrw:Gestion', default='N')
    return_back = String('mrw:Retorno', default='N')
    immediate_confirmation = String('mrw:ConfirmacionInmediata', default='N')
    reimbursement = String('mrw:Reembolso', default='N')


class GetLabel(Model):
    root_tag = None

    shipping_number = String('mrw:NumeroEnvio')
    delimiter = String('mrw:SeparadorNumerosEnvio', ignore_if_none=True)
    date_range_start = String('mrw:FechaInicioEnvio', ignore_if_none=True)
    date_range_end = String('mrw:FechaFinEnvio', ignore_if_none=True)
    label_type = String('mrw:TipoEtiquetaEnvio', default='0')
    top_margin = String('mrw:ReportTopMargin', default='1100')
    left_margin = String('mrw:ReportLeftMargin', default=650)


class SendResponseResult(Model):
    root_tag = None

    message = String('{http://www.mrw.es/}Mensaje')
    shipping_number = String('{http://www.mrw.es/}NumeroEnvio')
    request_number = String('{http://www.mrw.es/}NumeroSolicitud')
    status = String('{http://www.mrw.es/}Estado')
    url = String('{http://www.mrw.es/}Url')


class SendResponse(Model):
    root_tag = '{http://www.mrw.es/}TransmEnvioResponse'
    result = Nested(
        '{http://www.mrw.es/}TransmEnvioResult',
        SendResponseResult,
        unwrap=True
    )


class LabelResponseResult(Model):
    root_tag = None

    file = String('{http://www.mrw.es/}EtiquetaFile')
    message = String('{http://www.mrw.es/}Mensaje')
    status = String('{http://www.mrw.es/}Estado')


class LabelResponse(Model):
    root_tag = '{http://www.mrw.es/}GetEtiquetaEnvioResponse'
    result = Nested(
        '{http://www.mrw.es/}GetEtiquetaEnvioResult',
        LabelResponseResult,
        unwrap=True
    )
