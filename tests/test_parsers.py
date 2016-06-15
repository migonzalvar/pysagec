import pytest

from pysagec import parsers


def test_parser_simple():
    stream = (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root></root>'
    )
    parser = parsers.XMLParser()
    data = parser.parse(stream)
    assert {'root': None} == data


def test_parser_simple_with_namespace():
    stream = (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root xmlns="http://example.com"></root>'
    )
    parser = parsers.XMLParser()
    data = parser.parse(stream)
    assert {'{http://example.com}root': None} == data


def test_parser_one_children():
    stream = (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root><tag>Value</tag></root>'
    )
    parser = parsers.XMLParser()
    data = parser.parse(stream)
    assert {'root': [{'tag': 'Value'}]} == data


def test_parser_one_children_with_two_namespaces():
    stream = (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root'
        b' xmlns="http://example.com"'
        b' xmlns:ns="http://example.org">'
        b'<ns:tag>Value</ns:tag>'
        b'</root>'
    )
    parser = parsers.XMLParser()
    data = parser.parse(stream)
    assert ({
        '{http://example.com}root': [{'{http://example.org}tag': 'Value'}]
    }) == data


def test_parser_many_children():
    stream = (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root><tag1>Value 1</tag1><tag2>Value 2</tag2></root>'
    )
    parser = parsers.XMLParser()
    data = parser.parse(stream)
    assert {'root': [{'tag1': 'Value 1'}, {'tag2': 'Value 2'}]} == data


def test_parser_nested():
    stream = (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root><children>'
        b'<child1>Value 1</child1><child2>Value 2</child2>'
        b'</children></root>'
    )
    parser = parsers.XMLParser()
    data = parser.parse(stream)
    assert ({'root': [{
        'children': [{'child1': 'Value 1'}, {'child2': 'Value 2'}]}
    ]}) == data


def test_parser_error():
    bad_stream = (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root><tag1>Value 1</tag2>'
    )
    parser = parsers.XMLParser()
    with pytest.raises(parsers.ParseError):
        parser.parse(bad_stream)
