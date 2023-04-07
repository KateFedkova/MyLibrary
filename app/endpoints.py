from flask import make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import json
from app import app
from .services import book_info, add_user, convert_obj_to_str, search_info_by_title, \
    search_info_by_author, search_info_by_category
from .database import session, Users, WishList, Reviews


@app.route("/signup", methods=["GET", "POST"])
def signup():
    request_data = json.loads(request.data)
    user = session.query(Users).where(Users.username == request_data['username']).first()

    if user:
        response = make_response({"isReg": False, "reason": "already exists"}, 409)
        return response

    password = generate_password_hash(request_data["password"])
    user = Users(username=request_data["username"], password=password)
    add_user(user)

    response = make_response({"isReg": True}, 200)
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    request_data = json.loads(request.data)
    user = session.query(Users).where(Users.username == request_data["username"]).first()

    if user and check_password_hash(user.password, request_data["password"]):
        token = create_access_token(identity=user.id, expires_delta=timedelta(days=30))
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
    title = request_data["title"].lower().capitalize()
    user_id = get_jwt_identity()
    book = session.query(WishList).where(WishList.title == title, WishList.user_id == user_id).first()

    if book:
        response = make_response({"isAdded": False, "reason": "already exists"})
        response.status_code = 401
        return response

    new_book = WishList(title=title, author=request_data["author"].lower().capitalize(), user_id=user_id)
    add_user(new_book)

    response = make_response({"isAdded": True})
    response.status_code = 200
    return response


@app.route("/get_books", methods=["GET", "POST"])
@jwt_required()
def get_books():
    user_id = get_jwt_identity()
    user_books = session.query(WishList).where(WishList.user_id == user_id).all()
    jsonified = []

    for i in user_books:
        json_dict = convert_obj_to_str(i)
        jsonified.append(json_dict)

    response = make_response(jsonify(jsonified))
    return response


@app.route("/add_review", methods=["GET", "POST"])
@jwt_required()
def add_review():
    request_data = json.loads(request.data)
    user_id = get_jwt_identity()
    review = session.query(Reviews).where(Reviews.review == request_data["review"],
                                          Reviews.user_id == user_id).first()

    if review:
        response = make_response({"isAdded": False, "reason": "already exists"})
        response.status_code = 401
        return response

    new_review = Reviews(title=request_data["book-title"], author=request_data["book-author"],
                      review=request_data["review"], date_added=datetime.utcnow(), user_id=user_id)
    add_user(new_review)
    response = make_response({"isAdded": True})
    response.status_code = 200
    return response


@app.route("/get_reviews", methods=["GET", "POST"])
@jwt_required()
def get_reviews():
    user_id = get_jwt_identity()
    user_reviews = session.query(Reviews).where(Reviews.user_id == user_id).order_by(Reviews.date_added.desc()).all()
    jsonified = []

    for i in user_reviews:
        json_dict = convert_obj_to_str(i, True)
        jsonified.append(json_dict)

    response = make_response(jsonify(jsonified))
    return response


@app.route("/get_username", methods=["GET", "POST"])
@jwt_required()
def get_username():
    user_id = get_jwt_identity()
    name = session.query(Users).where(Users.id == user_id).first()
    json_dict = convert_obj_to_str(name)
    response = make_response(jsonify(json_dict))
    return response


@app.route("/change_info", methods=["GET", "POST"])
@jwt_required()
def change_info():
    request_data = json.loads(request.data)
    user_id = get_jwt_identity()
    user = session.query(Users).where(Users.id == user_id).first()

    if user.username != request_data["username"] and not request_data["password"]:
        user.username = request_data["username"]
        session.commit()
        response = make_response({"username is changed": True})
        return response

    elif request_data["password"] and user.username == request_data["username"]:
        user.password = generate_password_hash(request_data["password"])
        session.commit()
        response = make_response({"password is changed": True})
        return response

    if user.username != request_data["username"] and request_data["password"]:
        user.username = request_data["username"]
        user.password = generate_password_hash(request_data["password"])
        session.commit()
        response = make_response({"username and password are changed": True})
        return response


@app.route("/search", methods=["GET", "POST"])
def search():
    request_data = json.loads(request.data)
    option = request_data["select-items"]
    title = request_data["search-by-title"].lower().replace(" ", "+")
    author = request_data["search-by-author"].lower().replace(" ", "+")

    if option == "title":
        description, subject_places, subjects, subject_times = search_info_by_title(title)
        response_dict = {"title": request_data["search-by-title"], "description": description, "subject_places": subject_places, "subjects": subjects, "subject_times": subject_times}
        response = make_response(jsonify(response_dict))
        return response

    elif option == "author":
        all_books = search_info_by_author(author)
        books = book_info(all_books)
        response = make_response(jsonify(books))
        return response

    else:
        all_books = search_info_by_category(request_data["category"])
        books = book_info(all_books)
        response = make_response(jsonify(books))
        return response
