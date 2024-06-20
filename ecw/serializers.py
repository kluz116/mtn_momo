# myapp/serializers.py
from rest_framework import serializers
from .models import PaymentInstructionRequest, TransactionTimestamp, Amount

class TransactionTimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionTimestamp
        fields = ['timestamp']

class AmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amount
        fields = ['amount', 'currency']

class PaymentInstructionRequestSerializer(serializers.ModelSerializer):
    transactiontimestamp = TransactionTimestampSerializer()
    amount = AmountSerializer()

    class Meta:
        model = PaymentInstructionRequest
        fields = [
            'transactiontimestamp', 'amount', 'paymentinstructionid',
            'receiverbankcode', 'receiveraccountnumber', 'receiverfirstname',
            'receiversurname', 'message','transmissioncounter','transactionid',
        ]

    def create(self, validated_data):
        transactiontimestamp_data = validated_data.pop('transactiontimestamp')
        amount_data = validated_data.pop('amount')
        transactiontimestamp = TransactionTimestamp.objects.create(**transactiontimestamp_data)
        amount = Amount.objects.create(**amount_data)
        payment_instruction_request = PaymentInstructionRequest.objects.create(
            transactiontimestamp=transactiontimestamp, amount=amount, **validated_data
        )
        return payment_instruction_request
