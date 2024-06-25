import json
import time
from datetime import datetime

import requests
import xmltodict

from ecw.constants import *
from ecw.encrypt import *


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
    return json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4)


def get_account_holder_info(phone_number):
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

    response = requests.post(getaccountholderinfo_url, headers=headers, data=payload, cert=(certificate_path, key_path),
                             verify=False)
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


def get_account_holder_info_deposits(phone_number):
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

    response = requests.post(getaccountholderinfo_url, headers=headers, data=payload, cert=(certificate_path, key_path),
                             verify=False)
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


def deposit_funds(bankcode, accountnumber, amount, transactiontimestamp, currency, phone_number, banktransactionid,
                  message):
    receiver = f'FRI:{phone_number}/MSISDN'
    accountholder_info = get_account_holder_info_deposits(phone_number)

    if accountholder_info == 'ACCOUNTHOLDER_NOT_FOUND':
        return 'ACCOUNTHOLDER_NOT_FOUND'

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
