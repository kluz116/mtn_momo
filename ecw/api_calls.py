import time
from datetime import datetime
import requests
from django.http import request
from requests import RequestException

from ecw.constants import *
from ecw.encrypt import *
import xmltodict
import json

from ecw.models import AppLogs


def close_all_sessions():
    payload = json.dumps({
        "ourBranchID": ourBranchID,
        "operatorID": operatorID
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.post(close_session_url, headers=headers, data=payload)
    return response.json()


def get_access_token():
    close_all_sessions()
    payload = json.dumps({
        "userID": operatorID,
        "password": password,
        "branchID": ourBranchID,
        "systemID": "eee"
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.post(token, headers=headers, data=payload)
    return response.json().get("accessToken")


def getsigningcertificate():
    random_challenge = generate_random_challenge()
    time_stamp = round(time.time())
    final_str = f'{random_challenge};{time_stamp}'
    values_to_beSigned = f'{random_challenge};{time_stamp};'.encode('utf-8')

    x = signMsg(values_to_beSigned)
    yy = f'{final_str};{x}'

    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<ns0:getsigningcertificaterequest xmlns:ns0=\"http://www.ericsson.com/em/emm/messagesigning/v1_0\"/>"
    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': yy,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    response = requests.request("POST", getsigningcertificate_url, headers=headers, data=payload,
                                cert=(certificate_path, key_path), verify=False)

    return json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4)


def get_signing_certificate():
    random_challenge = generate_random_challenge()
    timestamp = round(time.time())
    values_to_be_signed = f'{random_challenge};{timestamp};'.encode('utf-8')
    signature = signMsg(values_to_be_signed)
    signature_header = f'{random_challenge};{timestamp};{signature}'

    payload = """<?xml version="1.0" encoding="UTF-8"?>
    <ns0:getsigningcertificaterequest xmlns:ns0="http://www.ericsson.com/em/emm/messagesigning/v1_0"/>"""

    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': signature_header,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    response = requests.post(getsigningcertificate_url, headers=headers, data=payload,
                             cert=(certificate_path, key_path), verify=False)

    obj_logs = {"url": getsigningcertificate_url, "headers": headers, "body": payload}
    obj = AppLogs.objects.create(**obj_logs)
    obj.save()
    return json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4)


def get_account_holder_info(phone_number):
    try:
        random_challenge = generate_random_challenge()
        timestamp = round(time.time())
        values_to_be_signed = f'{random_challenge};{timestamp};'.encode('utf-8')
        signature = signMsg(values_to_be_signed)
        signature_header = f'{random_challenge};{timestamp};{signature}'

        payload = f"""<?xml version="1.0" encoding="UTF-8"?>
        <ns0:getaccountholderinforequest xmlns:ns0="http://www.ericsson.com/em/emm/provisioning/v1_2">
            <identity>ID:{phone_number}/MSISDN</identity>
        </ns0:getaccountholderinforequest>"""

        headers = {
            'Content-Type': 'text/xml',
            'X-Signature': signature_header,
            'X-Original-Signer': 'ID:FTBbank/USER',
            'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
        }

        response = requests.post(getaccountholderinfo_url, headers=headers, data=payload,
                                 cert=(certificate_path, key_path), verify=False)
        response.raise_for_status()  # Raise HTTPError for bad responses

        obj_logs = {"url": getaccountholderinfo_url, "headers": headers, "body": payload}
        write_to_file(str(obj_logs))
        obj = AppLogs.objects.create(**obj_logs)
        obj.save()

        obj_response = json.loads(json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4))

        if "ns2:errorResponse" in obj_response:
            return obj_response["ns2:errorResponse"]["@errorcode"]

        accountholder_info = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"]
        return {
            "firstname": accountholder_info["firstname"],
            "surname": accountholder_info["surname"],
            "msisdn": accountholder_info["msisdn"],
            "accountholderstatus": accountholder_info["accountholderstatus"],
            "profilename": accountholder_info["profilename"],
            "msg": f"Successfully found {accountholder_info['msisdn']}"
        }

    except RequestException as e:
        error_message = f"An error occurred: {str(e)}"
        write_to_file(error_message)
        return 'error'


def get_account_holder_info_deposits(phone_number):
    try:
        random_challenge = generate_random_challenge()
        timestamp = round(time.time())
        values_to_be_signed = f'{random_challenge};{timestamp};'.encode('utf-8')
        signature = signMsg(values_to_be_signed)
        signature_header = f'{random_challenge};{timestamp};{signature}'

        payload = f"""<?xml version="1.0" encoding="UTF-8"?>
        <ns0:getaccountholderinforequest xmlns:ns0="http://www.ericsson.com/em/emm/provisioning/v1_2">
            <identity>ID:{phone_number}/MSISDN</identity>
        </ns0:getaccountholderinforequest>"""

        headers = {
            'Content-Type': 'text/xml',
            'X-Signature': signature_header,
            'X-Original-Signer': 'ID:FTBbank/USER',
            'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
        }

        response = requests.post(getaccountholderinfo_url, headers=headers, data=payload,
                                 cert=(certificate_path, key_path), verify=False)
        response.raise_for_status()  # Raise HTTPError for bad responses

        obj_logs = {"url": getaccountholderinfo_url, "headers": headers, "body": payload}
        obj = AppLogs.objects.create(**obj_logs)
        obj.save()

        obj_response = json.loads(json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4))

        if "ns2:errorResponse" in obj_response:
            return obj_response["ns2:errorResponse"]["@errorcode"]

        accountholder_info = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"]
        return {
            "firstname": accountholder_info["firstname"],
            "surname": accountholder_info["surname"],
            "msisdn": accountholder_info["msisdn"],
            "accountholderstatus": accountholder_info["accountholderstatus"]
        }

    except RequestException as e:
        error_message = f"An error occurred: {str(e)}"
        write_to_file(error_message)
        return "error"


def deposit_funds(bankcode, accountnumber, amount, transactiontimestamp, currency, phone_number, banktransactionid,
                  message):
    receiver = f'FRI:{phone_number}/MSISDN'
    accountholder_info = get_account_holder_info_deposits(phone_number)

    if accountholder_info == 'ACCOUNTHOLDER_NOT_FOUND':
        return 'ACCOUNTHOLDER_NOT_FOUND'

    if accountholder_info == 'INTERNAL_ERROR':
        return 'INTERNAL_ERROR'

    if accountholder_info == 'error':
        return 'Connectivity Error,System can not reach MTN'

    receiverfirstname = accountholder_info["firstname"]
    receiversurname = accountholder_info["surname"]

    random_challenge = generate_random_challenge()
    timestamp = round(time.time())
    values_to_be_signed = f'{random_challenge};{timestamp};{bankcode};{accountnumber};{amount};{currency};{receiver};{banktransactionid}'.encode(
        'utf-8')
    signature = signMsg(values_to_be_signed)
    signature_header = f'{random_challenge};{timestamp};{signature}'

    payload = f"""<ns2:depositrequest xmlns:ns2="http://www.ericsson.com/em/emm/settlement/v1_0">
    <bankcode>{bankcode}</bankcode>
    <accountnumber>{accountnumber}</accountnumber>
    <transactiontimestamp>
        <timestamp>{transactiontimestamp}</timestamp>
    </transactiontimestamp>
    <amount>
        <amount>{amount}</amount>
        <currency>{currency}</currency>
    </amount>
    <receiver>{receiver}</receiver>
    <banktransactionid>{banktransactionid}</banktransactionid>
    <receiverfirstname>{receiverfirstname}</receiverfirstname>
    <receiversurname>{receiversurname}</receiversurname>
    <message>{message}</message>
    </ns2:depositrequest>"""

    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': signature_header,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    response = requests.post(deposit_url, headers=headers, data=payload, cert=(certificate_path, key_path),
                             verify=False)

    obj_logs = {"url": deposit_url, "headers": headers, "body": payload}
    write_to_file(str(obj_logs))
    obj = AppLogs.objects.create(**obj_logs)
    obj.save()

    deposit_response = json.loads(json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4))

    if "ns2:errorResponse" in deposit_response:
        return deposit_response["ns2:errorResponse"]["@errorcode"]

    if "ns4:depositresponse" in deposit_response and deposit_response["ns4:depositresponse"]["status"] == "SUCCESS":
        return {
            "receiverfirstname": receiverfirstname,
            "receiversurname": receiversurname,
            "status": deposit_response["ns4:depositresponse"]["status"],
            "financialtransactionid": deposit_response["ns4:depositresponse"]["financialtransactionid"]
        }

    return 'Error, contact system administrator'


def deposit_funds_external(bankcode, accountnumber, amount, transactiontimestamp, currency, phone_number,
                           banktransactionid, message):
    receiver = f'FRI:{phone_number}/ext'
    random_challenge = generate_random_challenge()
    timestamp = round(time.time())
    values_to_be_signed = f'{random_challenge};{timestamp};{bankcode};{accountnumber};{amount};{currency};{receiver};{banktransactionid}'.encode(
        'utf-8')
    signature = signMsg(values_to_be_signed)
    signature_header = f'{random_challenge};{timestamp};{signature}'

    payload = f"""<ns2:depositrequest xmlns:ns2="http://www.ericsson.com/em/emm/settlement/v1_0">
    <bankcode>{bankcode}</bankcode>
    <accountnumber>{accountnumber}</accountnumber>
    <transactiontimestamp>
        <timestamp>{transactiontimestamp}</timestamp>
    </transactiontimestamp>
    <amount>
        <amount>{amount}</amount>
        <currency>{currency}</currency>
    </amount>
    <receiver>{receiver}</receiver>
    <banktransactionid>{banktransactionid}</banktransactionid>
    <receiverfirstname></receiverfirstname>
    <receiversurname></receiversurname>
    <message>{message}</message>
    </ns2:depositrequest>"""

    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': signature_header,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    response = requests.post(deposit_url, headers=headers, data=payload, cert=(certificate_path, key_path),
                             verify=False)

    obj_logs = {"url": deposit_url, "headers": headers, "body": payload}
    write_to_file(str(obj_logs))
    obj = AppLogs.objects.create(**obj_logs)
    obj.save()

    deposit_response = json.loads(json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4))

    if "ns2:errorResponse" in deposit_response:
        return deposit_response["ns2:errorResponse"]["@errorcode"]

    if "ns4:depositresponse" in deposit_response and deposit_response["ns4:depositresponse"]["status"] == "SUCCESS":
        return {
            "receiverfirstname": "",
            "receiversurname": "",
            "status": deposit_response["ns4:depositresponse"]["status"],
            "financialtransactionid": deposit_response["ns4:depositresponse"]["financialtransactionid"]
        }

    return 'Error, contact system administrator'


def date_formatter(transactiontimestamp):
    date_str = transactiontimestamp
    date_obj = datetime.strptime(date_str, '%Y%m%d%H%M%S')
    formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


def amount_formatter(amount):
    amount_str = str(amount)
    integer_part = amount_str[:-2]
    fractional_part = amount_str[-2:]
    formatted_amount = f'{integer_part}.{fractional_part}'
    return formatted_amount


def confirmation_message(phone_number, date, amount, financialtransactionid):
    return f'Transaction successful for {phone_number} on {date} for {amount} and the transaction ID is {financialtransactionid}'


def nimbleCreditCustomer(AccountID, Amount, trx_description):
    payload = json.dumps({
        "TrxBranchID": "206",
        "TrxBatchID": None,
        "SerialID": None,
        "OurBranchID": "206",
        "AccountTypeID": "C",
        "AccountID": AccountID,
        "ProductID": "803",
        "ModuleID": "3000",
        "TrxTypeID": "CC",
        "TrxDate": "2024-05-04 00:00:00",
        "Amount": Amount,
        "LocalAmount": Amount,
        "TrxCurrencyID": "UGX",
        "TrxAmount": Amount,
        "ExchangeRate": "1.0000",
        "MeanRate": "1.0000",
        "Profit": "0",
        "InstrumentTypeID": "V",
        "ChequeID": "0",
        "ChequeDate": None,
        "ReferenceNo": "",
        "Remarks": trx_description,
        "TrxDescriptionID": "001",
        "TrxDescription": trx_description,
        "MainGLID": 1,
        "ContraGLID": "100005",
        "TrxFlagID": "",
        "ImageID": "0",
        "TrxPrinted": "0",
        "CreatedBy": "CM2056",
        "UpdateCount": "2",
        "BREFTChargeID": None,
        "BREFTTrxID": None,
        "ReversalID": "0",
        "SupervisedBy": None,
        "SupervisedOn": None,
        "ChargeOnExcessAmount": "0",
        "IsChargeWaived": "false",
        "TrxCodeID": "0",
        "ValueDate": "2024-05-04 00:00:00",
        "ForwardRemark": "",
        "ErrorNo": "",
        "MainRowID": 0,
        "BranchType": "",
        "ActionID": None,
        "OtherDetails": "",
        "ActionTypeID": "I",
        "TillID": "3",
        "AccountTagID": None,
        "Denominations": None,
        "CostCenterID": "99",
        "ContraTillID": 0,
        "DeletedBy": None,
        "DeletedOn": None,
        "DeletedReason": None,
        "ApiActionTypeID": 2,
        "ApiActionID": 0,
        "ApiDynamicFields": None,
        "ApiModuleID": 3000,
        "ApiOperatorID": "CM2056",
        "ApiOurBranchID": "206",
        "ApiRequestID": None,
        "ApiRoleID": "SBO",
        "ApiUniqueID": "15348267561754039961",
        "ApiOperatedOn": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "ApiBankID": None,
        "ApiSearchKey": None,
        "RecentActivityModuleID": None,
        "RecentActivityControls": None,
        "RecentActivityControlValues": None
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_access_token()}'
    }

    try:
        response = requests.post(nimble_add_cash_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except RequestException as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return "error"


def paymentinstructionresponserequest_withdraw(status, paymentinstructionid, banktransactionid, amount, currency,
                                               transactiontimestamp, bookingtimestamp):
    random_challenge = generate_random_challenge()
    timestamp = round(time.time())
    signature_string = f'{random_challenge};{timestamp}'
    values_to_be_signed = f'{random_challenge};{timestamp};{status};{paymentinstructionid};{banktransactionid};{amount};{currency}'.encode(
        'utf-8')

    signature = signMsg(values_to_be_signed)
    signature_header = f'{signature_string};{signature}'

    payload = f"""
    <ns4:paymentinstructionresponserequest xmlns:ns4="http://www.ericsson.com/em/emm/settlement/v1_0">
        <status>{status}</status>
        <paymentinstructionid>{paymentinstructionid}</paymentinstructionid>
        <banktransactionid>{banktransactionid}</banktransactionid>
        <transactiontimestamp>
            <timestamp>{transactiontimestamp}</timestamp>
        </transactiontimestamp>
        <bookingtimestamp>
            <timestamp>{bookingtimestamp}</timestamp>
        </bookingtimestamp>
        <amount>
            <amount>{amount}</amount>
            <currency>{currency}</currency>
        </amount>
    </ns4:paymentinstructionresponserequest>
    """

    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': signature_header,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    response = requests.post(paymentinstructionresponse_url, headers=headers, data=payload,
                             cert=(certificate_path, key_path), verify=False)

    print(response.text)

    obj_logs = {"url": paymentinstructionresponserequest_url, "headers": headers, "body": payload}
    write_to_file(str(obj_logs))
    obj = AppLogs.objects.create(**obj_logs)
    obj.save()

    response_dict = xmltodict.parse(response.text, process_namespaces=False)
    response_json = json.dumps(response_dict, indent=4)

    withdraw_response = json.loads(response_json)

    print(withdraw_response)

    if "ns2:errorResponse" in withdraw_response:
        return withdraw_response["ns2:errorResponse"]["@errorcode"]
    else:
        return response.text


def nimbleTransferCreditCustomer(AccountID, Amount, trx_description, SerialID):
    payload = json.dumps({
        "AccountID": AccountID,
        "AccountTypeID": "C",
        "Amount": Amount,
        "ChequeID": "0",
        "CostCenterID": "99",
        "DontReturnSerial": "False",
        "ExchangeRate": "1.0",
        "ForwardRemark": None,
        "InstrumentTypeID": "V",
        "LocalAmount": Amount,
        "MainGLID": "1",
        "MeanRate": "1.0",
        "ModuleID": "3020",
        "OperatorID": "DK0657",
        "OtherDetails": "[]",
        "OurBranchID": "206",
        "PortfolioAccountID": None,
        "PortfolioBranchID": None,
        "PortfolioSeries": "0",
        "ProductID": "251",
        "Profit": "0.0",
        "ReferenceNo": trx_description,
        "Remarks": trx_description,
        "SerialID": SerialID,
        "SlNo": "0",
        "TrxAmount": Amount,
        "TrxBranchID": "211",
        "TrxCodeID": "0",
        "TrxCurrencyID": "UGX",
        "TrxDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "TrxDescription": trx_description,
        "TrxDescriptionID": "007",
        "TrxFlagID": None,
        "TrxTypeID": "TC",
        "ValueDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    })

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_access_token()}'
    }

    try:
        response = requests.post(transfer_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except RequestException as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return "error"


def nimbleTransferDebitCustomer(AccountID, Amount, trx_description, SerialID):
    payload = json.dumps({
        "AccountID": AccountID,
        "AccountTypeID": "C",
        "Amount": Amount,
        "ChequeID": "0",
        "CostCenterID": "99",
        "DontReturnSerial": "False",
        "ExchangeRate": "1.0",
        "ForwardRemark": "",
        "InstrumentTypeID": "V",
        "LocalAmount": Amount,
        "MainGLID": '1',
        "MeanRate": "1.0",
        "ModuleID": "3020",
        "OperatorID": "DK0657",
        "OtherDetails": "[]",
        "OurBranchID": "206",
        "PortfolioAccountID": None,
        "PortfolioBranchID": None,
        "PortfolioSeries": "0",
        "ProductID": "803",
        "Profit": "0.0",
        "ReferenceNo": trx_description,
        "Remarks": trx_description,
        "SerialID": SerialID,
        "SlNo": "1",
        "TrxAmount": Amount,
        "TrxBranchID": "211",
        "TrxCodeID": "0",
        "TrxCurrencyID": "UGX",
        "TrxDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "TrxDescription": trx_description,
        "TrxDescriptionID": "007",
        "TrxFlagID": None,
        "TrxTypeID": "TD",
        "ValueDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_access_token()}'
    }

    try:
        response = requests.post(transfer_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except RequestException as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return "error"


def AddTransferTransaction(serial_id, trx_branchid):
    payload = json.dumps({
        "ModuleID": "3020",
        "OperatorID": "DK0657",
        "SerialID": serial_id,
        "TrxBranchID": trx_branchid
    })
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {get_access_token()}'
    }
    try:
        response = requests.request("POST", AddTransferTransaction_url, headers=headers, data=payload)
        return response.json()


    except RequestException as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        return "error"
