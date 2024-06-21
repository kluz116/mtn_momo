from rest_framework_xml.renderers import XMLRenderer


class PaymentInstructionResponseXMLRenderer(XMLRenderer):
    root_tag_name = 'ns2:paymentinstructionresponse'
    item_tag_name = 'paymentinstructionresponse'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'ns2:paymentinstructionresponse': {
                'xmlns:ns2': 'http://www.ericsson.com/em/emm/settlement/v2_0',
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
                    'amount': data['amount']['amount'],
                    'currency': data['amount']['currency']
                }
            }
        }
        return super().render(response_data, accepted_media_type, renderer_context)
