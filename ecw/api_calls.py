from datetime import datetime

import requests

from ecw.constants import paymentinstructionresponse, certificate_path, key_path, deposit
from ecw.encrypt import *
import xmltodict
import json


def closeAllSession():
    url = "http://10.255.201.179:8092/api/v1/Common/CloseAllSessions"

    payload = json.dumps({
        "ourBranchID": "206",
        "operatorID": "CM2056"
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()

    print(res)


def getAccessToken():
    closeAllSession()
    url = "http://10.255.201.179:8093/api/v1/Token/LoginUser"

    payload = json.dumps({
        "userID": "CM2056",
        "password": "New@12345",
        "branchID": "206",
        "systemID": "eee"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    res = response.json()
    return res["accessToken"]


def getsigningcertificate():
    random_challenge = generate_random_challenge()
    time_stamp = round(time.time())
    final_str = f'{random_challenge};{time_stamp}'
    values_to_beSigned = f'{random_challenge};{time_stamp};'.encode('utf-8')

    x = signMsg(values_to_beSigned)
    yy = f'{final_str};{x}'

    url = "https://212.88.125.201:8027/banks/getsigningcertificate"
    cert_path = 'E:/ftb_uat_mtls/ftb_uat_mtls.crt'
    key_path = 'E:/ftb_uat_mtls/fintrust_signing_uat.key'

    payload = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<ns0:getsigningcertificaterequest xmlns:ns0=\"http://www.ericsson.com/em/emm/messagesigning/v1_0\"/>"
    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': yy,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cert=(cert_path, key_path), verify=False)
    # print(response.text)
    print(json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4))


def getAccontHolderInfo(phone_nmber):
    random_challenge = generate_random_challenge()
    time_stamp = round(time.time())
    final_str = f'{random_challenge};{time_stamp}'
    values_to_beSigned = f'{random_challenge};{time_stamp};'.encode('utf-8')

    x = signMsg(values_to_beSigned)
    yy = f'{final_str};{x}'

    url = "https://212.88.125.201:8027/banks/getaccountholderinfo"
    cert_path = 'E:/ftb_uat_mtls/ftb_uat_mtls.crt'
    key_path = 'E:/ftb_uat_mtls/fintrust_signing_uat.key'

    payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<ns0:getaccountholderinforequest xmlns:ns0=\"http://www.ericsson.com/em/emm/provisioning/v1_2\">\r\n    <identity>ID:{phone_nmber}/MSISDN</identity>\r\n</ns0:getaccountholderinforequest>"
    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': yy,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cert=(cert_path, key_path), verify=False)

    results = json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4)
    print(results)
    obj_response = json.loads(results)

    firstname = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"]["firstname"]
    surname = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"]["surname"]
    msisdn = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"]["msisdn"]
    accountholderstatus = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"][
        "accountholderstatus"]
    profilename = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"]["profilename"]

    return {"firstname": firstname, "surname": surname, "msisdn": msisdn,
            "accountholderstatus": accountholderstatus, "profilename": profilename, "msg": f"Successful found {msisdn}"}


def getAccontHolderInfoDeposits(phone_nmber):
    random_challenge = generate_random_challenge()
    time_stamp = round(time.time())
    final_str = f'{random_challenge};{time_stamp}'
    values_to_beSigned = f'{random_challenge};{time_stamp};'.encode('utf-8')

    x = signMsg(values_to_beSigned)
    yy = f'{final_str};{x}'

    url = "https://212.88.125.201:8027/banks/getaccountholderinfo"
    cert_path = 'E:/ftb_uat_mtls/ftb_uat_mtls.crt'
    key_path = 'E:/ftb_uat_mtls/fintrust_signing_uat.key'

    payload = f"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<ns0:getaccountholderinforequest xmlns:ns0=\"http://www.ericsson.com/em/emm/provisioning/v1_2\">\r\n    <identity>ID:{phone_nmber}/MSISDN</identity>\r\n</ns0:getaccountholderinforequest>"
    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': yy,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cert=(cert_path, key_path), verify=False)
    print(response.text)
    results = json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4)

    obj_response = json.loads(results)
    firstname = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"]["firstname"]
    surname = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"]["surname"]
    msisdn = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"]["msisdn"]
    accountholderstatus = obj_response["ns5:getaccountholderinforesponse"]["accountholderbasicinfo"][
        "accountholderstatus"]

    return {"firstname": firstname,
            "surname": surname,
            "msisdn": msisdn,
            "accountholderstatus": accountholderstatus}


def depositFunds(bankcode, accountnumber, amount, transactiontimestamp, currency, phone_number, banktransactionid,
                 message):
    receiver = f'FRI:{phone_number}/MSISDN'
    obj_response = getAccontHolderInfoDeposits(phone_number)
    receiverfirstname = obj_response["firstname"]
    receiversurname = obj_response["surname"]

    random_challenge = generate_random_challenge()
    time_stamp = round(time.time())
    final_str = f'{random_challenge};{time_stamp}'
    values_to_beSigned = f'{random_challenge};{time_stamp};{bankcode};{accountnumber};{amount};{currency};{receiver};{banktransactionid}'.encode(
        'utf-8')

    x = signMsg(values_to_beSigned)
    yy = f'{final_str};{x}'

    url = "https://212.88.125.201:8027/banks/deposit"
    cert_path = 'E:/ftb_uat_mtls/ftb_uat_mtls.crt'
    key_path = 'E:/ftb_uat_mtls/fintrust_signing_uat.key'

    payload = f"<ns2:depositrequest xmlns:ns2=\"http://www.ericsson.com/em/emm/settlement/v1_0\">\r\n    <bankcode>{bankcode}</bankcode>\r\n    <accountnumber>{accountnumber}</accountnumber>\r\n    <transactiontimestamp>\r\n        <timestamp>{transactiontimestamp}</timestamp>\r\n    </transactiontimestamp>\r\n    <amount>\r\n        <amount>{amount}</amount>\r\n        <currency>{currency}</currency>\r\n    </amount>\r\n    <receiver>{receiver}</receiver>\r\n    <banktransactionid>{banktransactionid}</banktransactionid>\r\n    <receiverfirstname>{receiverfirstname}</receiverfirstname>\r\n    <receiversurname>{receiversurname}</receiversurname>\r\n    <message>{message}</message>\r\n</ns2:depositrequest>"

    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': yy,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    response = requests.request("POST", url, headers=headers, data=payload, cert=(cert_path, key_path), verify=False)
    print(response.text)
    results = json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4)
    deposit_response = json.loads(results)
    status = deposit_response["ns4:depositresponse"]["status"]
    financialtransactionid = deposit_response["ns4:depositresponse"]["financialtransactionid"]

    return {"receiverfirstname": receiverfirstname,
            "receiversurname": receiversurname,
            "status": status,
            "financialtransactionid": financialtransactionid}


def depositFundsExternal(bankcode, accountnumber, amount, transactiontimestamp, currency, phone_number,
                         banktransactionid, message):
    receiver = f'FRI:{phone_number}/ext'

    random_challenge = generate_random_challenge()
    time_stamp = round(time.time())
    final_str = f'{random_challenge};{time_stamp}'
    values_to_beSigned = f'{random_challenge};{time_stamp};{bankcode};{accountnumber};{amount};{currency};{receiver};{banktransactionid}'.encode(
        'utf-8')

    x = signMsg(values_to_beSigned)
    yy = f'{final_str};{x}'

    payload = f"<ns2:depositrequest xmlns:ns2=\"http://www.ericsson.com/em/emm/settlement/v1_0\">\r\n    <bankcode>{bankcode}</bankcode>\r\n    <accountnumber>{accountnumber}</accountnumber>\r\n    <transactiontimestamp>\r\n        <timestamp>{transactiontimestamp}</timestamp>\r\n    </transactiontimestamp>\r\n    <amount>\r\n        <amount>{amount}</amount>\r\n        <currency>{currency}</currency>\r\n    </amount>\r\n    <receiver>{receiver}</receiver>\r\n    <banktransactionid>{banktransactionid}</banktransactionid>\r\n    <message>{message}</message>\r\n</ns2:depositrequest>"

    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': yy,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }

    print(payload)

    response = requests.request("POST", deposit, headers=headers, data=payload, cert=(certificate_path, key_path),
                                verify=False)
    print(response.text)
    results = json.dumps(xmltodict.parse(response.text, process_namespaces=False), indent=4)
    deposit_response = json.loads(results)
    status = deposit_response["ns4:depositresponse"]["status"]
    financialtransactionid = deposit_response["ns4:depositresponse"]["financialtransactionid"]

    return {
        "status": status,
        "financialtransactionid": financialtransactionid}


def nimbleCreditCustomer(AccountID, Amount, trx_description):
    url = "http://10.255.201.179:8092/api/v1/CashTransaction/AddCashTransaction"

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
        "TrxDate": "2024-05-04 00:00:00",  #datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
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
        "ValueDate": "2024-05-04 00:00:00",  #datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
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
        'Authorization': f'Bearer {getAccessToken()}'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.json()


def paymentinstructionresponserequest(random_challenge, status, paymentinstructionid, banktransactionid, amount,
                                      currency,
                                      bookingtimestamp, transactiontimestamp):
    time_stamp = round(time.time())
    final_str = f'{random_challenge};{time_stamp}'
    values_to_beSigned = f'{random_challenge};{time_stamp};{status};{paymentinstructionid};{banktransactionid};{amount};{currency}'.encode(
        'utf-8')

    x = signMsg(values_to_beSigned)
    yy = f'{final_str};{x}'

    payload = f"<ns2:paymentinstructionresponse xmlns:ns2=\"http://www.ericsson.com/em/emm/settlement/v2_0\">\r\n    <status>PENDING</status>\r\n    <paymentinstructionid>{paymentinstructionid}</paymentinstructionid>\r\n    <banktransactionid>{banktransactionid}</banktransactionid>\r\n    <transactiontimestamp>\r\n        <timestamp>{transactiontimestamp}</timestamp>\r\n    </transactiontimestamp>\r\n    <bookingtimestamp>\r\n        <timestamp>{bookingtimestamp}</timestamp>\r\n    </bookingtimestamp>\r\n    <amount>\r\n        <amount>{amount}</amount>\r\n        <currency>{currency}</currency>\r\n    </amount>\r\n</ns2:paymentinstructionresponse>"
    headers = {
        'Content-Type': 'text/xml',
        'X-Signature': yy,
        'X-Original-Signer': 'ID:FTBbank/USER',
        'Authorization': 'Basic RlRCYmFuazpBQmMxMjM0NTYh'
    }
    print(payload)

    response = requests.request("POST", paymentinstructionresponse, headers=headers, data=payload,
                                cert=(certificate_path, key_path), verify=False)
    return response.text
