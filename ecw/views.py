from decimal import Decimal
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
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

from .serializers import PaymentInstructionRequestSerializer
from .decorators import validate_signature
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


def addDeposit(request):
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
#@validate_signature(PUBLIC_KEY_PEM)
@csrf_exempt
@permission_classes([IsAuthenticated])
def paymentInstruction(request):
    x_signature = request.META.get('HTTP_X_SIGNATURE')
    paymentinstructionid = request.data['paymentinstructionid']
    transactiontimestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    bookingtimestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    banktransactionid = generate_random_trx_id()
    currency = request.data['amount']['currency']
    amount = request.data['amount']['amount']
    random_challenge = get_challenge(x_signature)
    response_status = 'PENDING'

    x_signature_obj = {
        "x_signature": x_signature,
        "paymentinstructionid": paymentinstructionid}

    serializer = PaymentInstructionRequestSerializer(data=request.data)
    if serializer.is_valid():
        #serializer.save()
        obj = Xsignature.objects.create(**x_signature_obj)
        obj.save()
        print('What is this', request.data['transactiontimestamp']['timestamp'])
        transaction_timestamp = TransactionTimestamp.objects.create(
            timestamp=request.data['transactiontimestamp']['timestamp'])
        amount = Amount.objects.create(amount=request.data['amount']['amount'])
        #currency = Amount.objects.create(amount=request.data['currency']['currency'])

        paymentinstruct = {'transactiontimestamp': transaction_timestamp,
                           'amount': amount,
                           'paymentinstructionid': request.data['paymentinstructionid'],
                           'receiverbankcode': request.data['receiverbankcode'],
                           'receiveraccountnumber': request.data['receiveraccountnumber'],
                           'receiverfirstname': request.data['receiverfirstname'],
                           'receiversurname': request.data['receiversurname'],
                           'message': request.data['message'],
                           'transmissioncounter': request.data['transmissioncounter'],
                           'transactionid': request.data['transactionid'],
                           'bookingtimestamp': bookingtimestamp,
                           'banktransactionid': banktransactionid,
                           'random_challenge': random_challenge,
                           'response_status': response_status
                           }

        payment_object = PaymentInstructionRequest.objects.create(**paymentinstruct)
        payment_object.save()
        responserequest = paymentinstructionresponserequest(random_challenge, response_status, paymentinstructionid,
                                                            banktransactionid, amount,
                                                            currency,
                                                            bookingtimestamp, transactiontimestamp)
        return Response(responserequest, status=status.HTTP_200_OK, content_type="text/xml")
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def getPaymentInstructions(request):
    dep = PaymentInstructionRequest.objects.all().order_by('-id')
    return render(request, 'ecw/paymentinstructions.html', {'dep': dep})


def PaymentInstructionsDetail(request):
    dep = PaymentInstructionRequest.objects.all().order_by('-id')
    return render(request, 'ecw/paymentinstructions.html', {'dep': dep})


@login_required(login_url='/ecw/')
def PaymentInstructionsDetail(request, id):
    sec = PaymentInstructionRequest.objects.get(id=id)
    '''if request.method == 'POST':
        form = PaymentForm(request.POST, instance=sec)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ecw/getPaymentInstructions')
    else:
        form = PaymentForm(instance=sec)'''
    return render(request, 'ecw/update_payment_instruction.html', {})
