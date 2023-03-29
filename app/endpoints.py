from flask import make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import app
import json
from .database import session, Users, WishList


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


@app.route("/login", methods=["GET", "POST"])
def login():
    request_data = json.loads(request.data)
    print(request_data)

    user = session.query(Users).where(Users.username == request_data["username"]).first()
    print(user)

    if user and check_password_hash(user.password, request_data["password"]):
        token = create_access_token(identity=user.id)
        response = make_response({"isLogged": True, "token": token})
        response.status_code = 200
        return response

    response = make_response({"isLogged": False})
    response.status_code = 401
    return response


@app.route("/add_book", methods=["GET", "POST"])
@jwt_required()
def add_book_to_list():
    request_data = json.loads(request.data)
    print(request_data)
    book = session.query(WishList).where(WishList.title == request_data["title"]).first()
    print(book)

    if book:
        response = make_response({"isAdded": False, "reason": "already exists"})
        response.status_code = 401
        return response

    new_book = WishList(title=request_data["title"], author=request_data["author"], user_id=get_jwt_identity())
    session.add(new_book)
    session.commit()

    response = make_response({"isAdded": True})
    response.status_code = 200
    return response


@app.route("/get_books", methods=["GET", "POST"])
@jwt_required()
def get_books():
    user_books = session.query(WishList).where(WishList.user_id == get_jwt_identity()).all()
    print(user_books)

    jsonified = []

    for i in user_books:
        converted = i.__dict__
        converted.pop('_sa_instance_state', None)
        print(converted)
        json_dict = json.dumps(converted)
        print(json_dict)
        jsonified.append(json_dict)
    print(jsonified)
    response = make_response(jsonify(jsonified))

    return response


