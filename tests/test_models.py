from pysagec import models


def test_auth_info():
    values = [
        ('mrw:CodigoFranquicia', 'franchise_code', '123456'),
        ('mrw:CodigoAbonado', 'subscriber_code', 'subscriber_code'),
        ('mrw:CodigoDepartamento', 'departament_code', 'departament_code'),
        ('mrw:UserName', 'username', 'username'),
        ('mrw:Password', 'password', 'password'),
    ]
    kwargs = {}
    expected = {'mrw:AuthInfo': []}
    for tag, prop, value in values:
        kwargs[prop] = value
        expected['mrw:AuthInfo'].append({tag: value})

    auth_info = models.AuthInfo(**kwargs)
    data = auth_info.as_dict()
    assert expected == data
