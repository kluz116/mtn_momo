# myapp/renderers.py
from rest_framework_xml.renderers import XMLRenderer


class CustomXMLRenderer(XMLRenderer):
    root_tag_name = 'ns4:paymentinstructionrequest' or 'ns4paymentinstructionrequest'
    media_type = 'text/xml'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        xml = super().render(data, accepted_media_type, renderer_context)

        # Remove the root element if it exists
        xml = xml.replace('<root>', '').replace('</root>', '')

        # Remove list-item tags if necessary
        xml = xml.replace('<list-item>', '').replace('</list-item>', '')

        return xml
