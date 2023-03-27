from flask import make_response, request
from werkzeug.security import generate_password_hash

from app import app
import json
from .database import session, Users


@app.route("/signup", methods=["GET", "POST"])
def signup():
    request_data = json.loads(request.data)
    print(request_data)
    user = session.query(Users).where(Users.username == request_data['username']).first()

    if user:
        response = make_response({"isReg": False, "reason": "already exists"}, 409)
        return response

    password = generate_password_hash(request_data["password"])
    #request_data["password"] = password
    user = Users(username=request_data["username"], password=password, quote=None)
    session.add(user)
    session.commit()

    response = make_response({"isReg": True}, 200)
    return response
