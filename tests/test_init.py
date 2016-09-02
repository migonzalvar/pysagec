from unittest.mock import patch, MagicMock


def test_create_client():
    import pysagec
    url = '//user:pass@example.com/?franchise=12&subscriber=34&department=56'
    client = pysagec.create_client(url)
    assert isinstance(client, pysagec.Client)
    assert client.auth_info.username == 'user'
    assert client.auth_info.password == 'pass'
    assert client.auth_info.franchise_code == '12'
    assert client.auth_info.subscriber_code == '34'
    assert client.auth_info.departament_code == '56'


@patch('pysagec.Client', MagicMock())
def test_readme_example():
    import pysagec
    import datetime as dt

    url = '//user:pass@example.com/?franchise=12&subscriber=34&department=56'

    client = pysagec.create_client(url)

    pickup_info = pysagec.PickupInfo(
        pickup_address=pysagec.Address(street_name='Plaza de España',
                                       postal_code='36001',
                                       city='Pontevedra'),
        recipient_name='Juan Pérez',
        recipient_phone_number='555555555',
        comments='Por las mañanas.',
    )

    service_info = pysagec.ServiceInfo(
        number_of_packages=1,
        date=dt.date.today(),
        service_code='0000',
    )

    response = client.send(pickup_info, service_info)

    print(response.shipping_number)
