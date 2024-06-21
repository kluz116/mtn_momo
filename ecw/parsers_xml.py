# myapp/parsers.py
from rest_framework_xml.parsers import XMLParser
import xml.etree.ElementTree as ET


class CustomXMLParser(XMLParser):
    media_type = 'text/xml'

    def parse(self, stream, media_type=None, parser_context=None):
        # Parse the XML and get rid of <root> and <list-item> tags
        parsed_data = super().parse(stream, media_type, parser_context)

        if 'root' in parsed_data:
            parsed_data = parsed_data['root']

        # Remove listitem tags if necessary (assuming they appear within a list)
        for key in parsed_data:
            if isinstance(parsed_data[key], list):
                parsed_data[key] = [item.get('list-item', item) for item in parsed_data[key]]

        return parsed_data
