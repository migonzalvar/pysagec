from pysagec.renderers import XMLRenderer


def test_xml_renderer_simple():
    renderer = XMLRenderer()
    stream = renderer.render({'root': None})
    assert '<?xml version="1.0" encoding="utf-8"?>\n<root></root>' == stream


def test_xml_renderer_nested():
    renderer = XMLRenderer()
    data = {'root': {'children': [{'child1': 'Mike'}, {'child2': 'Liza'}]}}
    stream = renderer.render(data)
    assert (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<root>'
        '<children><child1>Mike</child1><child2>Liza</child2></children>'
        '</root>'
    ) == stream
