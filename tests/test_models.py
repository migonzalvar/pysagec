from pysagec import models


def test_auth_info():
    kwargs = {'franchise_code': '123456',
              'subscriber_code': 'subscriber_code',
              'departament_code': 'departament_code',
              'username': 'username',
              'password': 'password'}
    auth_info = models.AuthInfo(**kwargs)
    data = auth_info.as_dict()
    expected = {'mrw:AuthInfo': [
        {'mrw:CodigoFranquicia': kwargs['franchise_code']},
        {'mrw:CodigoAbonado': kwargs['subscriber_code']},
        {'mrw:CodigoDepartamento': kwargs['departament_code']},
        {'mrw:UserName': kwargs['username']},
        {'mrw:Password': kwargs['password']},
    ]}
    assert expected == data
