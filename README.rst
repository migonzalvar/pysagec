=======
pysagec
=======

.. image:: https://travis-ci.org/migonzalvar/pysagec.svg?branch=master
   :target: https://travis-ci.org/migonzalvar/pysagec

.. image:: https://codecov.io/github/migonzalvar/pysagec/coverage.svg?branch=master
   :target: https://codecov.io/github/migonzalvar/pysagec?branch=master

**pysagec** is a Python library to use with SAGEC MRW webservices.

It aims to be simple to use but with the ability to use any of the fields
of the underlying API:

.. code:: python

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


Features
========

- Use python classes instead of XML.
- Simplify method invocation.
- It has no dependencies, only standard library.

Installation
============

Install **pysagec** `from PyPI`__:

__ https://pypi.python.org/pypi/pysagec

.. code:: console

    $ pip install pysagec


Change log
==========

Unreleased
----------

0.1.1 - 2016-09-02
------------------

- Add an example.

- Include more models into __init__.

0.1.0 - 2016-08-25
------------------

- First production ready release.

License
=======

MIT.
