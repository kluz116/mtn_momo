from rest_framework_xml.renderers import XMLRenderer
from xml.etree.ElementTree import Element, tostring
from xml.dom import minidom
from decimal import Decimal, ROUND_HALF_UP


class PaymentInstructionResponseXMLRenderer(XMLRenderer):
    root_tag_name = 'ns2:paymentinstructionresponse'
    namespace = 'http://www.ericsson.com/em/emm/settlement/v2_0'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'status': data['status'],
            'paymentinstructionid': data['paymentinstructionid'],
            'banktransactionid': data['banktransactionid'],
            'transactiontimestamp': {
                'timestamp': data['transactiontimestamp']['timestamp']
            },
            'bookingtimestamp': {
                'timestamp': data['bookingtimestamp']['timestamp']
            },
            'amount': {
                'amount': self.format_decimal(data['amount']['amount']),
                'currency': data['amount']['currency']
            }
        }

        # Generate the XML structure
        root = Element(self.root_tag_name)

        # Add namespace declaration
        root.set('xmlns:ns2', self.namespace)

        # Add child elements
        self._dict_to_xml(root, response_data)

        # Convert Element to XML string
        xml_string = tostring(root, encoding='utf-8', method='xml')

        # Prettify the XML string
        parsed_xml = minidom.parseString(xml_string)
        pretty_xml_string = parsed_xml.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')

        # Include XML declaration with standalone attribute
        final_xml_string = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + '\n'.join(
            pretty_xml_string.split('\n')[1:])

        return final_xml_string

    def _dict_to_xml(self, parent, data):
        for key, value in data.items():
            if isinstance(value, dict):
                # Recursively create sub-elements
                child = Element(key)
                parent.append(child)
                self._dict_to_xml(child, value)
            else:
                # Add text content for leaf elements
                child = Element(key)
                child.text = str(value)
                parent.append(child)

    def format_decimal(self, value):
        decimal_value = Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return str(decimal_value)
