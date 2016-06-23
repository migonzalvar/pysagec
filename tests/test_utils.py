from pysagec import utils


def test_base64_to_file(tmpdir):
    data = b'AA=='
    filename = tmpdir.join('file.pdf')
    assert not filename.exists(), 'Temporary file exists'
    utils.base64_to_file(data, filename.strpath)
    assert filename.exists()


def test_get_hostname_from_url():
    assert 'example.com' == utils.get_hostname_from_url('//example.com/')
