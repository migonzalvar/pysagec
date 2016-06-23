from pysagec import models


def test_models_are_instantiable():
    a = models.AuthInfo()
    assert isinstance(a, models.Model)


def test_create_auth_info_from_url():
    url = '//user:pass@example.com/?franchise=12&subscriber=34&department=56'
    auth_info = models.AuthInfo.from_url(url)
    assert isinstance(auth_info, models.AuthInfo)
    assert auth_info.username == 'user'
    assert auth_info.password == 'pass'
    assert auth_info.franchise_code == '12'
    assert auth_info.subscriber_code == '34'
    assert auth_info.departament_code == '56'
