from io import StringIO
from xml.sax.saxutils import XMLGenerator


class XMLRenderer:
    def render(self, data):
        stream = StringIO()

        xml = XMLGenerator(stream, encoding='utf-8')
        xml.startDocument()

        if isinstance(data, (list, tuple)):
            assert False, 'Renderer of iterables not supported yet'

        keys = list(data.keys())
        if len(keys) != 1:
            assert False, 'Data should only have one key to use it as root'

        root_element = keys[0]

        xml.startElement(root_element, {})  # TODO: add namespaces

        self._to_xml(xml, data[root_element])

        xml.endElement(root_element)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                self._to_xml(xml, item)

        elif isinstance(data, dict):
            for key, value in data.items():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)

        elif isinstance(data, bool):
            xml.characters('true' if data else 'false')

        elif data is None:
            # Don't output any value
            pass

        else:
            xml.characters(str(data))
