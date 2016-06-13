import pytest

from pysagec.renderers import XMLRenderer, RenderError


def test_xml_renderer_simple():
    renderer = XMLRenderer()
    stream = renderer.render({'root': None})
    assert b'<?xml version="1.0" encoding="utf-8"?>\n<root></root>' == stream


def test_xml_renderer_nested():
    renderer = XMLRenderer()
    data = {'root': {'children': [{'child1': 'Mike'}, {'child2': 'Liza'}]}}
    stream = renderer.render(data)
    assert (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root>'
        b'<children><child1>Mike</child1><child2>Liza</child2></children>'
        b'</root>'
    ) == stream


def test_xml_renderer_boolean():
    renderer = XMLRenderer()
    data = {'root': [{'yes': True}, {'no': False}]}
    stream = renderer.render(data)
    assert (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root><yes>true</yes><no>false</no></root>'
    ) == stream


def test_xml_render_raises_error_if_more_than_one_key_in_data():
    renderer = XMLRenderer()
    with pytest.raises(RenderError):
        renderer.render({'one': None, 'two': None})


def test_xml_render_raises_error_if_data_is_iterable():
    renderer = XMLRenderer()
    with pytest.raises(RenderError):
        renderer.render([{'one': None}, {'two': None}])


def test_xml_renderer_namespaces():
    renderer = XMLRenderer()
    namespaces = [('foo', 'http://example.com/ns')]
    stream = renderer.render({'root': None}, namespaces=namespaces)
    assert (
        b'<?xml version="1.0" encoding="utf-8"?>\n'
        b'<root xmlns:foo="http://example.com/ns"></root>'
    ) == stream
