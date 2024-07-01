import json


def getMessage(res):
    results_json_str = res['responseValue'][0]['results']
    results_dict = json.loads(results_json_str)
    message = results_dict['Message']
    return message


def getSystemMessage(res):
    results_json_str = res['responseValue'][0]['results']
    results_dict = json.loads(results_json_str)
    message = results_dict['SystemMessage']
    return message


def getMessageDB(res):
    results_json_str = res['responseValue'][0]['results']
    results_dict = json.loads(results_json_str)
    message = results_dict['SystemMessage']
    return message


def getbatchID(res):
    results_json_str = res['responseValue'][0]['results']
    results_dict = json.loads(results_json_str)
    trx_status_json_str = results_dict['TrxStatus']
    trx_status_dict = json.loads(trx_status_json_str)
    trx_batch_id = trx_status_dict['TrxBatchID']
    return trx_batch_id


def getSerialID(res):
    results_json_str = res['responseValue'][0]['results']
    results_dict = json.loads(results_json_str)
    trx_status_json_str = results_dict['TrxStatus']
    trx_status_dict = json.loads(trx_status_json_str)
    trx_Serial_id = trx_status_dict['SerialID']
    return trx_Serial_id


def getProductID(number):
    number_str = str(number)
    extracted_digits = number_str[3:6]
    extracted_number = int(extracted_digits)

    return extracted_number


def getOurBranchID(number):
    number_str = str(number)
    extracted_digits = number_str[0:3]
    extracted_number = int(extracted_digits)

    return extracted_number
