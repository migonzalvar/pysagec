from pysagec import *  # NOQA: on purpose to detect __all__ regressions


def test_create_client():
    url = '//user:pass@example.com/?franchise=12&subscriber=34&department=56'
    client = create_client(url)  # noqa: F405
    assert isinstance(client, Client)  # noqa: F405
    assert client.auth_info.username == 'user'
    assert client.auth_info.password == 'pass'
    assert client.auth_info.franchise_code == '12'
    assert client.auth_info.subscriber_code == '34'
    assert client.auth_info.departament_code == '56'
