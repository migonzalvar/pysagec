from pysagec import models


def test_auth_info():
    auth_info = models.AuthInfo()
    data = auth_info.as_dict()
    expected = {'mrw:AuthInfo': [
        {'mrw:CodigoFranquicia': ''},
        {'mrw:CodigoAbonado': ''},
        {'mrw:CodigoDepartamento': ''},
        {'mrw:UserName': ''},
        {'mrw:Password': ''},
    ]}
    assert expected == data
