from .base import Field, Model


class AuthInfo(Model):
    root_tag = 'mrw:AuthInfo'

    franchise_code = Field('mrw:CodigoFranquicia')
    subscriber_code = Field('mrw:CodigoAbonado')
    departament_code = Field('mrw:CodigoDepartamento')
    username = Field('mrw:UserName')
    password = Field('mrw:Password')
