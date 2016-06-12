class AuthInfo:
    def __init__(self, franchise_code, subscriber_code, departament_code,
                 username, password):
        self.subscriber_code = subscriber_code
        self.franchise_code = franchise_code
        self.departament_code = departament_code
        self.username = username
        self.password = password

    def as_dict(self):
        return {'mrw:AuthInfo': [
            {'mrw:CodigoFranquicia': self.franchise_code},
            {'mrw:CodigoAbonado': self.subscriber_code},
            {'mrw:CodigoDepartamento': self.departament_code},
            {'mrw:UserName': self.username},
            {'mrw:Password': self.password},
        ]}
