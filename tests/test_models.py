from pysagec import models


def test_auth_info():
    auth_info = models.AuthInfo()
    data = auth_info.as_dict()
    assert 'mrw:AuthInfo' in data
    elements = data['mrw:AuthInfo']
    assert len(elements) == 5
    keys = [
      'mrw:CodigoFranquicia',
      'mrw:CodigoAbonado',
      'mrw:CodigoDepartamento',
      'mrw:UserName',
      'mrw:Password',
    ]
    for key, element in zip(keys, elements):
        assert key in element
