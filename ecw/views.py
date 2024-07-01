import uuid
from decimal import Decimal
import pandas as pd
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_datetime
from rest_framework.permissions import IsAuthenticated
from .EcwForms import *
from .api_calls import *
from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .PaymentInstructionResponseXMLRenderer import PaymentInstructionResponseXMLRenderer
from .serializers import PaymentInstructionResponseSerializer
from .utility import *

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


@login_required(login_url='/ecw/')
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
            banktransactionid = str(uuid.uuid4())
            trx_password = form['trx_password'].value()
            trx_branchid = request.user.branch.branch_code if request.user.branch else None
            till_id = request.user.till.till_id if request.user.till else None
            operator_id = request.user.operator_id
            get_token = get_access_tokens(trx_branchid, operator_id, trx_password)

            trx_description = f'MTN Deposit Cash Deposit {amount} MSSIDN: {receiver} at {transactiontimestamp}'
            res = deposit_funds(bankcode, accountnumber, amount, transactiontimestamp, currency, receiver,
                                banktransactionid, trx_description)

            if res == 'TARGET_NOT_FOUND':
                messages.error(request, f"Phone number {receiver} not found")
            elif res == 'ACCOUNTHOLDER_NOT_FOUND':
                messages.error(request, f"ACCOUNTHOLDER_NOT_FOUND {receiver} ")
            elif res == 'INTERNAL_ERROR':
                messages.error(request, f"INTERNAL_ERROR")
            elif res == 'CUSTODY_ACCOUNT_NOT_FOUND':
                messages.error(request, f"CUSTODY_ACCOUNT_NOT_FOUND")
            elif res == 'AUTHORIZATION_MAXIMUM_AMOUNT_ALLOWED_TO_RECEIVE':
                messages.error(request, 'AUTHORIZATION_MAXIMUM_AMOUNT_ALLOWED_TO_RECEIVE')
            else:
                cash_control_gl = getCashControlGL(trx_branchid, operator_id, till_id, get_token)
                response = nimbleCreditCustomer("206803000001", amount, trx_description, trx_branchid, operator_id,
                                                cash_control_gl,receiver, get_token)

                if getMessage(response) == 'error':
                    messages.error(request, 'Ooops,can not reach core banking now.Contact system administrator')
                if getMessage(response) == 'Success' and getMessageDB(response) == '50000':
                    messages.error(request, 'Ooops,can not reach core banking now.Contact system administrator')

                if getMessage(response) == 'Success' and getMessageDB(response) != '50000':
                    first_name = res.get("receiverfirstname", "")
                    sur_name = res.get("receiversurname", "")
                    status = res.get("status", "")
                    financialtransactionid = res.get("financialtransactionid", "")
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
                        "message": trx_description,
                        "receiverfirstname": first_name,
                        "receiversurname": sur_name,
                        "status": status,
                        "trx_batchid": trx_batchid,
                        "trx_serialid": trx_serialid,
                        "financialtransactionid": financialtransactionid,
                        "trx_password": signPassword(trx_password),
                        "created_by": request.user
                    }

                    # Create DepositFunds object
                    obj = DepositFunds.objects.create(**deposit_obj_data)
                    obj.save()

                    # Display success message and redirect
                    messages.success(request,
                                     f'Successful deposit of {amount} UGX to {receiver} with status: {status}. TrxBatchID {trx_batchid} and SerialID {trx_serialid}')
                    return HttpResponseRedirect('/ecw/getDeposits')
                else:
                    messages.error(request, f"{getSystemMessage(response)}")
                    # Return response as JSON if nimbleCreditCustomer fails
                    #return JsonResponse(response)
    else:
        form = DepositForm()

    return render(request, 'ecw/create_deposit.html', {'form': form})


@login_required(login_url='/ecw/')
def addDepositExternalId(request):
    if request.method == 'POST':
        form = DepositFormExternal(request.POST)
        if form.is_valid():
            bankcode = form['bankcode'].value()
            accountnumber = form['accountnumber'].value()
            amount = form['amount'].value()
            receiver = form['receiver'].value()
            transactiontimestamp = form['transactiontimestamp'].value()
            currency = form['currency'].value()
            banktransactionid = str(uuid.uuid4())
            trx_password = form['trx_password'].value()
            trx_branchid = request.user.branch.branch_code if request.user.branch else None
            till_id = request.user.till.till_id if request.user.till else None
            operator_id = request.user.operator_id
            get_token = get_access_tokens(trx_branchid, operator_id, trx_password)

            trx_description = f'MTN Deposit Cash Deposit {amount} ExternalID: {receiver} at {transactiontimestamp}'
            res = deposit_funds_external(bankcode, accountnumber, amount, transactiontimestamp, currency, receiver,
                                         banktransactionid, trx_description)

            if res == 'TARGET_NOT_FOUND':
                messages.error(request, f"Phone number {receiver} not found")
            elif res == 'ACCOUNTHOLDER_NOT_FOUND':
                messages.error(request, f"ACCOUNTHOLDER_NOT_FOUND {receiver} ")
            elif res == 'INTERNAL_ERROR':
                messages.error(request, f"INTERNAL_ERROR")
            elif res == 'CUSTODY_ACCOUNT_NOT_FOUND':
                messages.error(request, f"CUSTODY_ACCOUNT_NOT_FOUND")
            elif res == 'AUTHORIZATION_MAXIMUM_AMOUNT_ALLOWED_TO_RECEIVE':
                messages.error(request, 'AUTHORIZATION_MAXIMUM_AMOUNT_ALLOWED_TO_RECEIVE')
            else:
                cash_control_gl = getCashControlGL(trx_branchid, operator_id, till_id, get_token)
                response = nimbleCreditCustomer("206803000001", amount, trx_description, trx_branchid, operator_id,
                                                cash_control_gl, receiver, get_token)

                if getMessage(response) == 'error':
                    messages.error(request, 'Ooops,can not reach core banking now.Contact system administrator')
                if getMessage(response) == 'Success' and getMessageDB(response) == '50000':
                    messages.error(request, 'Ooops,can not reach core banking now.Contact system administrator')

                if getMessage(response) == 'Success' and getMessageDB(response) != '50000':
                    first_name = res.get("receiverfirstname", "")
                    sur_name = res.get("receiversurname", "")
                    status = res.get("status", "")
                    financialtransactionid = res.get("financialtransactionid", "")
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
                        "message": trx_description,
                        "receiverfirstname": first_name,
                        "receiversurname": sur_name,
                        "status": status,
                        "trx_batchid": trx_batchid,
                        "trx_serialid": trx_serialid,
                        "financialtransactionid": financialtransactionid,
                        "trx_password": signPassword(trx_password),
                        "created_by": request.user
                    }

                    # Create DepositFunds object
                    obj = DepositFunds.objects.create(**deposit_obj_data)
                    obj.save()

                    # Display success message and redirect
                    messages.success(request,
                                     f'Successful deposit of {amount} UGX to {receiver} with status: {status}. TrxBatchID {trx_batchid} and SerialID {trx_serialid}')
                    return HttpResponseRedirect('/ecw/getDeposits')
                else:
                    messages.error(request, f"{getSystemMessage(response)}")
                    # Return response as JSON if nimbleCreditCustomer fails
                    #return JsonResponse(response)
    else:
        form = DepositFormExternal()

    return render(request, 'ecw/create_deposit_external.html', {'form': form})


@login_required(login_url='/ecw/')
def addDepositExternalId_old(request):
    if request.method == 'POST':
        form = DepositFormExternal(request.POST)
        if form.is_valid():
            bankcode = form['bankcode'].value()
            accountnumber = form['accountnumber'].value()
            amount = form['amount'].value()
            receiver = form['receiver'].value()
            transactiontimestamp = form['transactiontimestamp'].value()
            currency = form['currency'].value()
            banktransactionid = str(uuid.uuid4())

            trx_description = f'MTN Deposit Cash Deposit {amount} MSSIDN: {receiver} at {transactiontimestamp}'
            res = deposit_funds_external(bankcode, accountnumber, amount, transactiontimestamp, currency, receiver,
                                         banktransactionid, trx_description)

            if res == 'MISSING_ACTOR_MSISDN_FOR_EXTERNAL_RATING':
                messages.error(request, f"MISSING_ACTOR_MSISDN_FOR_EXTERNAL_RATING")
            elif res == 'INTERNAL_ERROR':
                messages.error(request, f"INTERNAL_ERROR")
            elif res == 'RESOURCE_NOT_FOUND':
                messages.error(request, 'RESOURCE_NOT_FOUND')
            else:
                response = nimbleCreditCustomer("206803000001", amount, trx_description)
                if getMessage(response) == 'Success':
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
                        "message": trx_description,
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

    return render(request, 'ecw/create_deposit_external.html', {'form': form})


@login_required(login_url='/ecw/')
def getDeposits(request):
    dep = DepositFunds.objects.all().order_by('-id')
    return render(request, 'ecw/deposits.html', {'dep': dep})


@login_required(login_url='/ecw/')
def addAccountHolder(request):
    form = AccountHolderForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            phone_nmber = form['msisdn'].value()
            res = get_account_holder_info(phone_nmber)
            print(res)

            if res == 'ACCOUNTHOLDER_NOT_FOUND':
                messages.error(request, f"{res}")
            elif res == 'INTERNAL_ERROR':
                messages.error(request, 'INTERNAL_ERROR')
            elif res == 'error':
                messages.error(request, 'Connectivity Error,System can not reach MTN')
            else:
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


@login_required(login_url='/ecw/')
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

        try:
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
            return payment_instruction_request_obj
        except IntegrityError:
            # Handle the error, e.g., return an error message
            Response("A PaymentInstructionRequest with this paymentinstructionid already exists.")

        time_stamp = round(time.time())
        final_str = f'{random_challenge};{time_stamp}'
        values_to_beSigned = f'{random_challenge};{time_stamp};{response_status};{paymentinstructionid};{banktransactionid};{amount_value};{currency}'.encode(
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
            verfySif(values_to_beSigned, x)
            obj_logs = {"url": paymentinstructionresponse_url, "headers": response.headers, "body": response.data}
            write_to_file(str(obj_logs))
            return response
        else:

            return Response(serializer_response.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/ecw/')
def getPaymentInstructions(request):
    dep = PaymentInstructionRequest.objects.all().order_by('-id')
    return render(request, 'ecw/paymentinstructions.html', {'dep': dep})


@login_required(login_url='/ecw/')
def PaymentInstructionsDetail(request):
    dep = PaymentInstructionRequest.objects.all().order_by('-id')
    return render(request, 'ecw/paymentinstructions.html', {'dep': dep})


@login_required(login_url='/ecw/')
def PaymentInstructionsDetail(request, id):
    sec = get_object_or_404(PaymentInstructionRequest, id=id)

    if request.method == 'POST':
        form = PaymentInstructionRequestForm(request.POST, instance=sec)
        if form.is_valid():

            paymentinstructionid = form['paymentinstructionid'].value()
            bookingtimestamp = form['bookingtimestamp'].value()
            banktransactionid = form['banktransactionid'].value()
            amount_value = form['amount_value'].value()
            transactiontimestamp_value = form['transactiontimestamp_value'].value()
            receiveraccountnumber = form['receiveraccountnumber'].value()
            trx_password = form['trx_password'].value()
            currency = 'UGX'
            trx_description = f'Paymentinstructionid: {paymentinstructionid} Amount: {amount_value} transactiontimestamp_value: {transactiontimestamp_value}  '
            SerialID = random.randint(100, 200)
            trx_branchid = request.user.branch.branch_code if request.user.branch else None
            operator_id = request.user.operator_id
            receiveraccountnumbers = "206209005703"
            product_id = getProductID(receiveraccountnumber)
            ourbranch_id = getOurBranchID(receiveraccountnumber)

            get_token = get_access_tokens(trx_branchid, operator_id, trx_password)
            response1 = nimbleTransferDebitCustomer(debit_account, amount_value, trx_description, SerialID, operator_id,
                                                    trx_branchid, get_token)
            if getMessage(response1) == 'Success':
                response2 = nimbleTransferCreditCustomer(receiveraccountnumbers, amount_value, trx_description,
                                                         SerialID, operator_id, trx_branchid, ourbranch_id, product_id,
                                                         get_token)
                if getMessage(response2) == 'Success':
                    response3 = AddTransferTransaction(SerialID, trx_branchid, operator_id, get_token)

                    if getMessage(response3) == 'Success':
                        response_status = 'SUCCESS'
                        # res = paymentinstructionresponserequest_withdraw(response_status, paymentinstructionid,
                        #banktransactionid,
                        #amount_value, currency,
                        #transactiontimestamp_value,
                        # bookingtimestamp)
                        res = ''
                        if res == 'SETTLEMENT_AMOUNT_DO_NOT_MATCH':
                            messages.error(request, f"SETTLEMENT_AMOUNT_DO_NOT_MATCH")
                        if res == 'Success':
                            instance = form.save()
                            instance.response_status = response_status
                            instance.trx_password = signPassword(trx_password)
                            instance.save()
                            messages.success(request,
                                             f'Fund transfer of {amount_value}{currency} to {receiveraccountnumber} now completed with TrxBatchID {getbatchID(response3)} and SeralID {getSerialID(response3)}')
                            return HttpResponseRedirect('/ecw/getPaymentInstructions')
                    else:
                        messages.error(request, f'{getSystemMessage(response3)}')

                else:
                    messages.error(request, "Unable to credit account")

            else:
                messages.error(request, "Unable to Debit account")

    else:
        form = PaymentInstructionRequestForm(instance=sec)

    return render(request, 'ecw/update_payment_instruction.html', {'form': form})


@login_required(login_url='/ecw/')
def generate_excel(request):
    form = DepositReportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            from_transactiontimestamp_value = form['from_transactiontimestamp_value'].value()
            to_transactiontimestamp_value = form['to_transactiontimestamp_value'].value()

            query = DepositFunds.objects.all()

            # Parse dates and filter queryset
            if from_transactiontimestamp_value and to_transactiontimestamp_value:
                try:
                    start_date = parse_datetime(to_transactiontimestamp_value)
                    end_date = parse_datetime(to_transactiontimestamp_value)
                    if start_date and end_date:
                        query = query.filter(transactiontimestamp__range=(start_date, end_date))
                    else:
                        return messages.error(request,
                                              'Invalid date format. Dates must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.')
                except ValueError:
                    messages.error(request,
                                   'Invalid date format. Dates must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.')

            # Convert the QuerySet to a DataFrame
            persons = query.values('bankcode', 'accountnumber', 'amount', 'receiver',
                                   'transactiontimestamp', 'currency', 'banktransactionid',
                                   'message', 'receiverfirstname', 'receiversurname',
                                   'status', 'trx_batchid', 'trx_serialid')
            df = pd.DataFrame(persons)

            # Convert datetime columns to timezone-unaware
            if 'transactiontimestamp' in df.columns:
                df['transactiontimestamp'] = pd.to_datetime(df['transactiontimestamp']).dt.tz_convert(None)

            # Create an HTTP response with the appropriate Excel headers
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename=desposits_{to_transactiontimestamp_value}.xlsx'

            # Use Pandas to write the DataFrame to an Excel file
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Deposits')

            return response
    return render(request, 'ecw/deposit_report.html', {'form': form})


@login_required(login_url='/ecw/')
def generate_excel_withdraw(request):
    form = WithdrawReportForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            from_transactiontimestamp_value = form['from_transactiontimestamp_value'].value()
            to_transactiontimestamp_value = form['to_transactiontimestamp_value'].value()

            query = PaymentInstructionRequest.objects.all()

            # Parse dates and filter queryset
            if from_transactiontimestamp_value and to_transactiontimestamp_value:
                try:
                    start_date = parse_datetime(to_transactiontimestamp_value)
                    end_date = parse_datetime(to_transactiontimestamp_value)
                    if start_date and end_date:
                        query = query.filter(bookingtimestamp__range=(start_date, end_date))
                    else:
                        return messages.error(request,
                                              'Invalid date format. Dates must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.')
                except ValueError:
                    messages.error(request,
                                   'Invalid date format. Dates must be in YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format.')

            # Convert the QuerySet to a DataFrame
            persons = query.values('paymentinstructionid', 'receiverbankcode', 'amount', 'receiveraccountnumber',
                                   'transactiontimestamp', 'transactionid', 'banktransactionid',
                                   'message', 'receiverfirstname', 'receiversurname',
                                   'response_status', 'transmissioncounter', 'bookingtimestamp')
            df = pd.DataFrame(persons)

            # Convert datetime columns to timezone-unaware
            if 'bookingtimestamp' in df.columns:
                df['bookingtimestamp'] = pd.to_datetime(df['bookingtimestamp']).dt.tz_convert(None)

            # Create an HTTP response with the appropriate Excel headers
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename=withdraw_{to_transactiontimestamp_value}.xlsx'

            # Use Pandas to write the DataFrame to an Excel file
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Deposits')

            return response
    return render(request, 'ecw/withdraw_report.html', {'form': form})


@login_required(login_url='/ecw/')
def addBranch(request):
    form = BranchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully added a branch.")
            return HttpResponseRedirect('/ecw/addBranch')
    return render(request, 'addBranch.html', {'form': form})


@login_required(login_url='/ecw/')
def getBranches(request):
    branch = Branch.objects.all().order_by('-id')
    return render(request, 'ecw/branches.html', {'branch': branch})


@login_required(login_url='/ecw/')
def addUsers(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return HttpResponseRedirect('/ecw/addUsers')
        else:
            form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, "ecw/addUsers.html", context)


@login_required(login_url='/ecw/')
def getEcwUsers(request):
    user = EcwUser.objects.all().order_by('-id')
    return render(request, "ecw/ecw_users.html", {'user': user})


@login_required(login_url='/ecw/')
def updateUser(request, id):
    sec = EcwUser.objects.get(id=id)

    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, instance=sec)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/ecw/addUsers')
    else:
        form = CustomUserEditForm(instance=sec)
    return render(request, 'ecw/edit_user.html', {'form': form})
