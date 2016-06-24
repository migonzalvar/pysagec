import pysagec


def test_create_client():
    url = '//user:pass@example.com/?franchise=12&subscriber=34&department=56'
    client = pysagec.create_client(url)
    assert isinstance(client, pysagec.Client)
    assert client.auth_info.username == 'user'
    assert client.auth_info.password == 'pass'
    assert client.auth_info.franchise_code == '12'
    assert client.auth_info.subscriber_code == '34'
    assert client.auth_info.departament_code == '56'
