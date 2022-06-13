from datetime import datetime, timedelta, timezone
from jwt import encode, decode
from config import variables
from jwt import exceptions
from flask import jsonify

def expireDate():
    expiration = datetime.now(tz=timezone.utc) + timedelta(seconds=600)
    return expiration

def writeToken(auth):
    token = encode(payload={**auth, "exp": expireDate()}, key=variables["SECRET_KEY"], algorithm="HS256")
    return token.encode("UTF-8")

def validateToken(token, output=False):
    try:
        decode(token, key=variables["SECRET_KEY"], algorithms = ["HS256"])
        if output:
            return True
    except exceptions.DecodeError:
        response  = jsonify({"message": "Invalid token."})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response  = jsonify({"message": "Token has expired."})
        response.status_code = 401
        return response