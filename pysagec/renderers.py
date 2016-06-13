from io import BytesIO
from xml.sax.saxutils import XMLGenerator


class RenderError(Exception):
    pass


class XMLRenderer:
    def render(self, data, namespaces=None):
        namespaces = namespaces or []
        stream = BytesIO()

        xml = XMLGenerator(stream, encoding='utf-8')
        xml.startDocument()

        if isinstance(data, (list, tuple)):
            raise RenderError('Renderer of iterables is not supported')

        keys = list(data.keys())
        if len(keys) != 1:
            raise RenderError('`data` should have only one key, the root')

        root_element = keys[0]

        attrs = {'xmlns:' + ns: url for ns, url in namespaces}
        xml.startElement(root_element, attrs)

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
