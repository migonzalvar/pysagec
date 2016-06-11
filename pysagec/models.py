class AuthInfo:
    def as_dict(self):
        return {'mrw:AuthInfo': [
            {'mrw:CodigoFranquicia': ''},
            {'mrw:CodigoAbonado': ''},
            {'mrw:CodigoDepartamento': ''},
            {'mrw:UserName': ''},
            {'mrw:Password': ''},
        ]}
