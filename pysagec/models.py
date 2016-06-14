from .base import Model, Nested, String


class AuthInfo(Model):
    root_tag = 'mrw:AuthInfo'

    franchise_code = String('mrw:CodigoFranquicia')
    subscriber_code = String('mrw:CodigoAbonado')
    departament_code = String('mrw:CodigoDepartamento', ignore_if_none=True)
    username = String('mrw:UserName')
    password = String('mrw:Password')


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
    contact__phone_number = String('mrw:Contacto')
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
