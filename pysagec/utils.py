import base64


def base64_to_file(data, filename):
    data = base64.b64decode(data)
    with open(filename, 'wb') as fp:
        fp.write(data)
