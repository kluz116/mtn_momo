import uuid
from decimal import Decimal
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .EcwForms import *
from .api_calls import *
from rest_framework.decorators import api_view, parser_classes, renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .PaymentInstructionResponseXMLRenderer import PaymentInstructionResponseXMLRenderer
from .serializers import PaymentInstructionRequestSerializer, PaymentInstructionResponseSerializer
from xml.sax.saxutils import unescape
from .utility import getMessage, getbatchID, getSerialID

PUBLIC_KEY_PEM = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAm9PLCmsiOn/IqzDAcILS
ENe0ftsFbncpI4t7UMwtNFHAzZQFMpkyGeKB+UBBWED+vt2JknG86JCl4DkB2yab
sdgQLT3L9En1/OvqcWV7VNrENzhyGDx86Hc0XXSyPnURA4L4qzCUmgATDdwj4Ggi
U0BOQstLQ0fVajB70p13h3orqkrGzLjfCHGIRwDtYo29gunpCcuygTxuJUm+oUlR
YmqZQleg8pb/7eqYUzM7rpS3ul40GepTKlp3A9H8yn2NCHSSXQ5wOBxUWem4bKn9
eRz/u+bj+phX435VcpSkprXeOWgorBFoKKclvHYUgTfnf99EX6dGa5Y7Hjg2NdSy
MwIDAQAB
-----END PUBLIC KEY-----
"""


# Create your views here.
def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("getDeposits")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name='ecw/login.html', context={"login_form": form})


def logout_request_metropol(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return HttpResponseRedirect('/ecw/')


@login_required(login_url='/ecw/')
def getIndex(request):
    return render(request, 'index.html', {})


def addDepositxxx(request):
    form = DepositForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            bankcode = form['bankcode'].value()
            accountnumber = form['accountnumber'].value()
            amount = form['amount'].value()
            receiver = form['receiver'].value()
            transactiontimestamp = form['transactiontimestamp'].value()
            currency = form['currency'].value()
            #banktransactionid = form['banktransactionid'].value()
            message = form['message'].value()
            banktransactionid = generate_random_trx_id()
            trx_description = f'MTN Deposit Cash Deposit {amount} MSSIDN: {receiver} at {transactiontimestamp}'

            response = nimbleCreditCustomer("206803000001", amount, trx_description)

            if getMessage(response) == 'Success':
                res = depositFunds(bankcode, accountnumber, amount, transactiontimestamp, currency, receiver,
                                   banktransactionid, message)

                first_name = res["receiverfirstname"]
                sur_name = res["receiversurname"]
                status = res["status"]

                trx_batchid = getbatchID(response)
                trx_serialid = getSerialID(response)

                deposit_obj_data = {
                    "bankcode": bankcode,
                    "accountnumber": accountnumber,
                    "amount": amount,
                    "receiver": receiver,
                    "transactiontimestamp": transactiontimestamp,
                    "currency": currency,
                    "banktransactionid": banktransactionid,
                    "message": message,
                    "receiverfirstname": first_name,
                    "receiversurname": sur_name,
                    "status": status,
                    "trx_batchid": trx_batchid,
                    "trx_serialid": trx_serialid}

                obj = DepositFunds.objects.create(**deposit_obj_data)
                obj.save()
                messages.success(request,
                                 f'Successful deposit of {amount} UGX to {receiver} with status :{status}. TrxBatchID {trx_batchid} and SerailID {trx_serialid}')
                return HttpResponseRedirect('/ecw/getDeposits')
            else:
                return JsonResponse(response)
    return render(request, 'create_deposit.html', {'form': form})


def addDeposit(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            bankcode = form['bankcode'].value()
            accountnumber = form['accountnumber'].value()
            amount = form['amount'].value()
            receiver = form['receiver'].value()
            transactiontimestamp = form['transactiontimestamp'].value()
            currency = form['currency'].value()
            message = form['message'].value()
            banktransactionid = str(uuid.uuid4())

            trx_description = f'MTN Deposit Cash Deposit {amount} MSSIDN: {receiver} at {transactiontimestamp}'

            # Call nimbleCreditCustomer and check response
            response = nimbleCreditCustomer("206803000001", amount, trx_description)
            if getMessage(response) == 'Success':
                # Call depositFunds and get response
                res = depositFunds(bankcode, accountnumber, amount, transactiontimestamp, currency, receiver,
                                   banktransactionid, message)

                if res == 'TARGET_NOT_FOUND':
                    messages.warning(request, f"Phone number {receiver} not found")
                else:
                    # Extract necessary data from response
                    first_name = res.get("receiverfirstname", "")
                    sur_name = res.get("receiversurname", "")
                    status = res.get("status", "")
                    trx_batchid = getbatchID(response)
                    trx_serialid = getSerialID(response)

                    # Prepare data for DepositFunds object
                    deposit_obj_data = {
                        "bankcode": bankcode,
                        "accountnumber": accountnumber,
                        "amount": amount,
                        "receiver": receiver,
                        "transactiontimestamp": transactiontimestamp,
                        "currency": currency,
                        "banktransactionid": banktransactionid,
                        "message": message,
                        "receiverfirstname": first_name,
                        "receiversurname": sur_name,
                        "status": status,
                        "trx_batchid": trx_batchid,
                        "trx_serialid": trx_serialid
                    }

                    # Create DepositFunds object
                    obj = DepositFunds.objects.create(**deposit_obj_data)
                    obj.save()

                    # Display success message and redirect
                    messages.success(request,
                                     f'Successful deposit of {amount} UGX to {receiver} with status: {status}. TrxBatchID {trx_batchid} and SerialID {trx_serialid}')
                    return HttpResponseRedirect('/ecw/getDeposits')


            else:
                # Return response as JSON if nimbleCreditCustomer fails
                return JsonResponse(response)
    else:
        form = DepositForm()

    return render(request, 'create_deposit.html', {'form': form})


def addDepositExternalId(request):
    form = DepositFormExternal(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            bankcode = form['bankcode'].value()
            accountnumber = form['accountnumber'].value()
            amount = form['amount'].value()
            receiver = form['receiver'].value()
            transactiontimestamp = form['transactiontimestamp'].value()
            currency = form['currency'].value()
            #banktransactionid = form['banktransactionid'].value()
            message = form['message'].value()

            banktransactionid = generate_random_trx_id()
            trx_description = f'MTN Deposit Cash Deposit {amount} MSSIDN: {receiver} at {transactiontimestamp}'

            response = nimbleCreditCustomer("206803000001", amount, trx_description)

            if getMessage(response) == 'Success':
                res = depositFundsExternal(bankcode, accountnumber, amount, transactiontimestamp, currency, receiver,
                                           banktransactionid, message)

                status = res["status"]
                trx_batchid = getbatchID(response)
                trx_serialid = getSerialID(response)

                deposit_obj_data = {
                    "bankcode": bankcode,
                    "accountnumber": accountnumber,
                    "amount": amount,
                    "receiver": receiver,
                    "transactiontimestamp": transactiontimestamp,
                    "currency": currency,
                    "banktransactionid": banktransactionid,
                    "message": message,
                    "status": status,
                    "trx_batchid": trx_batchid,
                    "trx_serialid": trx_serialid
                }

                obj = DepositFunds.objects.create(**deposit_obj_data)
                obj.save()
                messages.success(request,
                                 f'Successful deposit of {amount} UGX to {receiver} with status :{status}. TrxBatchID {trx_batchid} and SerailID {trx_serialid}')
                return HttpResponseRedirect('/ecw/getDeposits')
    return render(request, 'ecw/create_deposit_external.html', {'form': form})


def getDeposits(request):
    dep = DepositFunds.objects.all().order_by('-id')
    return render(request, 'ecw/deposits.html', {'dep': dep})


def addAccountHolder(request):
    form = AccountHolderForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():

            phone_nmber = form['msisdn'].value()

            res = getAccontHolderInfo(phone_nmber)

            firstname = res['firstname']
            surname = res['surname']
            accountholderstatus = res['accountholderstatus']
            profilename = res['profilename']
            msisdn = res['msisdn']
            msg = res['msg']

            account_holder_obj_data = {
                "firstname": firstname,
                "surname": surname,
                "msisdn": msisdn,
                "accountholderstatus": accountholderstatus,
                "profilename": profilename}
            if msisdn == 'None':
                messages.success(request, f'{msg}')
            else:
                obj = AccountHolder.objects.create(**account_holder_obj_data)
                obj.save()

                return HttpResponseRedirect('/ecw/getAccountHolders')

    return render(request, 'ecw/add_account_holder.html', {'form': form})


def getAccountHolders(request):
    dep = AccountHolder.objects.all().order_by('-id')
    return render(request, 'ecw/account_holders.html', {'dep': dep})


@api_view(['POST'])
@csrf_exempt
@permission_classes([IsAuthenticated])
@renderer_classes([PaymentInstructionResponseXMLRenderer])
def paymentInstruction(request):
    try:


        x_signature = request.META.get('HTTP_X_SIGNATURE')
        paymentinstructionid = request.data.get('paymentinstructionid')
        transactiontimestamp = request.data.get('transactiontimestamp', {}).get('timestamp', datetime.now().strftime(
            "%Y-%m-%dT%H:%M:%S"))
        bookingtimestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        banktransactionid = str(uuid.uuid4())
        currency = request.data.get('amount', {}).get('currency')
        amount_value = request.data.get('amount', {}).get('amount')
        random_challenge = get_challenge(x_signature)
        response_status = 'PENDING'

        x_signature_obj = {
            "x_signature": x_signature,
            "paymentinstructionid": paymentinstructionid
        }

        # Save Xsignature object
        x_signature_instance = Xsignature.objects.create(**x_signature_obj)

        # Create transaction timestamp object
        transaction_timestamp_instance = TransactionTimestamp.objects.create(
            timestamp=transactiontimestamp
        )

        # Create amount object
        amount_instance = Amount.objects.create(
            amount=amount_value,
            currency=currency
        )

        # Create PaymentInstructionRequest object
        payment_instruction_request_obj = PaymentInstructionRequest.objects.create(
            transactiontimestamp=transaction_timestamp_instance,
            amount=amount_instance,
            paymentinstructionid=paymentinstructionid,
            receiverbankcode=request.data.get('receiverbankcode'),
            receiveraccountnumber=request.data.get('receiveraccountnumber'),
            receiverfirstname=request.data.get('receiverfirstname'),
            receiversurname=request.data.get('receiversurname'),
            message='',
            transmissioncounter=request.data.get('transmissioncounter'),
            transactionid=request.data.get('transactionid'),
            bookingtimestamp=bookingtimestamp,
            banktransactionid=banktransactionid,
            random_challenge=random_challenge,
            response_status=response_status
        )

        time_stamp = round(time.time())
        final_str = f'{random_challenge};{time_stamp}'
        values_to_beSigned = f'{random_challenge};{time_stamp};{status};{paymentinstructionid};{banktransactionid};{amount_value};{currency}'.encode(
            'utf-8')

        x = signMsg(values_to_beSigned)
        yy = f'{final_str};{x}'
        original_signer = 'ID:FTBbank/USER'

        # Serialize PaymentInstructionResponse
        response_obj = {
            'transactiontimestamp': {'timestamp': transactiontimestamp},
            'amount': {'amount': Decimal(amount_value), 'currency': currency},
            'bookingtimestamp': {'timestamp': bookingtimestamp},
            'paymentinstructionid': paymentinstructionid,
            'status': response_status,
            'banktransactionid': banktransactionid
        }

        serializer_response = PaymentInstructionResponseSerializer(data=response_obj)

        if serializer_response.is_valid():
            response = Response(serializer_response.data, status=status.HTTP_200_OK, content_type='text/xml')
            response['X-Signature'] = yy
            response['X-Original-Signer'] = original_signer

            return response
        else:
            return Response(serializer_response.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def getPaymentInstructions(request):
    dep = PaymentInstructionRequest.objects.all().order_by('-id')
    return render(request, 'ecw/paymentinstructions.html', {'dep': dep})


def PaymentInstructionsDetail(request):
    dep = PaymentInstructionRequest.objects.all().order_by('-id')
    return render(request, 'ecw/paymentinstructions.html', {'dep': dep})


@login_required(login_url='/ecw/')
def PaymentInstructionsDetail(request, id):
    sec = get_object_or_404(PaymentInstructionRequest, id=id)

    if request.method == 'POST':
        form = PaymentInstructionRequestForm(request.POST, instance=sec)
        if form.is_valid():
            form.save()
            messages.info(request, f'Successful Withdraw')
            return HttpResponseRedirect('/ecw/getPaymentInstructions')
    else:
        form = PaymentInstructionRequestForm(instance=sec)

    return render(request, 'ecw/update_payment_instruction.html', {'form': form})
