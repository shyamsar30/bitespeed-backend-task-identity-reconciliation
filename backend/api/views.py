from backend.api.responses import respond


def identify(data):
    return respond(200, "Success", {"data": "hii"})