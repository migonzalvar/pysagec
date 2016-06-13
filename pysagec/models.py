from .base import String, Model


class AuthInfo(Model):
    root_tag = 'mrw:AuthInfo'

    franchise_code = String('mrw:CodigoFranquicia')
    subscriber_code = String('mrw:CodigoAbonado')
    departament_code = String('mrw:CodigoDepartamento')
    username = String('mrw:UserName')
    password = String('mrw:Password')
