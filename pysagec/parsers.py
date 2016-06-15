from io import BytesIO
import xml.etree.ElementTree as etree


class ParseError(Exception):
    pass


class XMLParser:
    def parse(self, stream):
        parser = etree.XMLParser(encoding='utf-8')

        try:
            tree = etree.parse(BytesIO(stream), parser)
        except etree.ParseError as exc:
            raise ParseError(exc.msg)

        root = tree.getroot()
        data = self._xml_convert(root, unwrap=True)
        return {root.tag: data}

    def _xml_convert(self, element, unwrap=False):
        children = list(element)

        if len(children) > 0:
            data = []
            for child in children:
                data.append({child.tag: self._xml_convert(child, unwrap=True)})
            return {element.tag: data} if not unwrap else data

        # len(children) == 0
        return element.text
