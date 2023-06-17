from flask import jsonify
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException, NotFound


def respond(status_code, message="", payload=False):
    response_json={}
    if message:
        response_json["message"] = message
    if payload:
        response_json["payload"] = payload
    if bool(response_json) is False:
        raise Exception("Either message or payload is required.")
    
    response = jsonify(response_json)   
    response.status_code = status_code
    return response

def handle_exceptions(exception):
    if isinstance(exception, ValidationError):
        return respond(400, "Validation Error", exception.messages)
    elif isinstance(exception, NotFound):
        return Exception
    elif isinstance(exception, HTTPException):
        return Exception
    
    raise Exception

    return respond(400, "Server Error", str(exception))