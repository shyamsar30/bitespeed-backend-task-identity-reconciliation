from flask import jsonify
from backend.api.responses import respond
from backend.database.dao import user_dao_handler
from backend.database.datatypes import LinkPrecedenceTypes

def identify(data):

    email = data.get('email')
    phoneNumber = data.get('phoneNumber')

    complete_record = user_dao_handler.get_complete_record(email, phoneNumber)

    if complete_record:
        return generate_response(email, phoneNumber)


    partial_record = user_dao_handler.get_partital_record(email, phoneNumber)

    if not partial_record:
        record = {
            "email": email,
            "phoneNumber": phoneNumber,
            "linkPrecedence": LinkPrecedenceTypes.PRIMARY
        }
        user_dao_handler.insert_record(record)
        return generate_response(email, phoneNumber)
    
    if (not email) or (not phoneNumber):
        return generate_response(email, phoneNumber)
    
    records = [
        {
            "id": _.id,
            "phoneNumber": _.phoneNumber,
            "email": _.email,
            "linkedId": _.linkedId,
            "linkPrecedence": _.linkPrecedence
        }
        for _ in partial_record
    ]

    isEmailFound = False
    isPhoneFound = False

    link_id = records[0].get("id")
    
    if records[0].get('email') == email:
        isEmailFound = True
    if records[0].get('phoneNumber') == phoneNumber:
        isPhoneFound = True

    for record in records[1:]:
        if record.get('linkPrecedence') != LinkPrecedenceTypes.SECONDARY:
            row_data = {
                "id": record['id'],
                "phoneNumber": record['phoneNumber'],
                "email": record['email'],
                "linkedId": link_id,
                "linkPrecedence": LinkPrecedenceTypes.SECONDARY
            }
            user_dao_handler.insert_record(row_data)
        
        if not isEmailFound:
            if record.get('email') == email:
                isEmailFound = True
        if not isPhoneFound:
            if record['phoneNumber'] == phoneNumber:
                isPhoneFound = True

    if (not isEmailFound) or (not isPhoneFound):
        row_data = {
            "phoneNumber": phoneNumber,
            "email": email,
            "linkedId": link_id,
            "linkPrecedence": LinkPrecedenceTypes.SECONDARY
        }
        user_dao_handler.insert_record(row_data)

    return generate_response(email, phoneNumber)

def get_unique_emails(data):
    temp = []
    if data[0].email:
        temp.append(data[0].email)

    for d in data[1:]:
        if d.email and d.email not in temp:
            temp.append(d.email)

    return temp

def get_unique_phoneNumbers(data):
    temp = []
    if data[0].phoneNumber:
        temp.append(data[0].phoneNumber)

    for d in data[1:]:
        if d.phoneNumber and d.phoneNumber not in temp:
            temp.append(d.phoneNumber)

    return temp


def generate_response(email, phoneNumber):
    ids = set()
    record_ids = user_dao_handler.get_ids_from_email_phone(email, phoneNumber)

    for record in record_ids:
        ids.add(record.id)
        if record.linkedId:
            ids.add(record.linkedId)

    record_ids = user_dao_handler.get_ids_from_ids(ids)

    for record in record_ids:
        ids.add(record.id)
        if record.linkedId:
            ids.add(record.linkedId)

    previous_n = -1

    while previous_n < len(ids):
        previous_n = len(ids)
        record_ids = user_dao_handler.get_ids_from_ids(ids)

        for record in record_ids:
            ids.add(record.id)
            if record.linkedId:
                ids.add(record.linkedId)

    records = user_dao_handler.get_records_by_ids(ids)

    payload = {
        "contact": {
            "primaryContatctId": records[0].id,
            "emails": get_unique_emails(records),
            "phoneNumbers": get_unique_phoneNumbers(records),
            "secondaryContactIds": [_.id for _ in records[1:]]
        }
    }

    response = jsonify(payload)
    response.status_code = 200

    return response
