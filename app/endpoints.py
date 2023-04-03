from flask import make_response, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import app
import json
from .database import session, Users, WishList, Reviews
from datetime import datetime, timedelta
import requests
from .services import book_info


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


@app.route("/add_review", methods=["GET", "POST"])
@jwt_required()
def add_review():
    request_data = json.loads(request.data)
    print(request_data)
    review = session.query(Reviews).where(Reviews.review == request_data["review"]).first()
    print(review)

    if review:
        response = make_response({"isAdded": False, "reason": "already exists"})
        response.status_code = 401
        return response

    new_review = Reviews(title=request_data["book-title"], author=request_data["book-author"],
                      review=request_data["review"], date_added=datetime.utcnow(), user_id=get_jwt_identity())
    session.add(new_review)
    session.commit()

    response = make_response({"isAdded": True})
    response.status_code = 200
    return response


@app.route("/get_reviews", methods=["GET", "POST"])
@jwt_required()
def get_reviews():
    #user_reviews = session.query(Reviews).where(Reviews.user_id == get_jwt_identity()).all().order_by(Reviews.date_added)
    user_reviews = session.query(Reviews).where(Reviews.user_id == get_jwt_identity()).order_by(Reviews.date_added.desc()).all()
    print(user_reviews)

    jsonified = []

    for i in user_reviews:
        converted = i.__dict__
        converted.pop('_sa_instance_state', None)
        print(converted)
        converted.pop("date_added", None)
        json_dict = json.dumps(converted)
        print(json_dict)
        jsonified.append(json_dict)
    print(jsonified)
    response = make_response(jsonify(jsonified))
    return response


@app.route("/get_username", methods=["GET", "POST"])
@jwt_required()
def get_username():
    name = session.query(Users).where(Users.id == get_jwt_identity()).first()
    print(name)

    converted = name.__dict__
    converted.pop('_sa_instance_state', None)

    json_dict = json.dumps(converted)
    print(json_dict)
    print(type(json_dict))
    print(type(jsonify(json_dict)))

    response = make_response(jsonify(json_dict))
    return response


@app.route("/change_info", methods=["GET", "POST"])
@jwt_required()
def change_info():

    request_data = json.loads(request.data)
    print(request_data)
    user = session.query(Users).where(Users.id == get_jwt_identity()).first()
    response = make_response()

    if user.username != request_data["username"]:
        user.username = request_data["username"]
        session.commit()
        response = make_response({"username is changed": True})

    elif request_data["password"]:
        user.password = generate_password_hash(request_data["password"])
        session.commit()
        response = make_response({"password is changed": True})

    elif user.username != request_data["username"] and request_data["password"]:
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
    #print(title)
    if option == "title":
        description, subject_places, subjects, subject_times = search_info_by_title(title)
        #print(description, subject_places, subjects, subject_times)
        response_dict = {"title": title, "description": description, "subject_places": subject_places, "subjects": subjects, "subject_times": subject_times}
        #print(response_dict)
        response = make_response(jsonify(response_dict))
        return response

    elif option == "author":
        all_books = search_info_by_author(author)
        books = book_info(all_books)

        response = make_response(jsonify(books))
        print("make response")
        return response

    else:



    #response = make_response({"hello": True})
    #return response


def search_info_by_title(title):
    books = requests.get(f"https://openlibrary.org/search.json?title={title}")
    book_key = books.json()["docs"][0]["key"]
    #info_book = requests.get(f"https://openlibrary.org/{book_key}.json")
    info_book = requests.get(f"https://openlibrary.org/{book_key}.json").json()
    # description = info_book.json()["description"] if True else info_book.json()["description"]["value"] else "No description found" if KeyError
    # subject_places = info_book.json()["subject_places"]
    # subjects = info_book.json()["subjects"]
    # subject_times = info_book.json()["subject_times"]
    # #author_key = info_book.json()["authors"][0]["author"]["key"]
    # #author = requests.get(f"https://openlibrary.org/{author_key}.json")
    # #print(author.json())
    # #fuller_name = author.json()["fuller_name"]
    # return description, subject_places, subjects, subject_times
    try:
        description = info_book["description"]["value"]
    except TypeError:
        description = info_book["description"]
    except KeyError:
        description = "No description found"
    try:
        subject_places = info_book["subject_places"]
    except KeyError:
        subject_places = "No subject places found"
    try:
        subjects = info_book["subjects"]
    except KeyError:
        subjects = "No subjects found"

    #subjects = info_book["subjects"]
    try:
        subject_times = info_book["subject_times"]
    except KeyError:
        subject_times = "No subject times found"

    # author_key = info_book.json()["authors"][0]["author"]["key"]
    # author = requests.get(f"https://openlibrary.org/{author_key}.json")
    # print(author.json())
    # fuller_name = author.json()["fuller_name"]
    return description, subject_places, subjects, subject_times


def search_info_by_author(author):
    author_info = requests.get(f"https://openlibrary.org/search.json?author={author}&limit=5")
    author_books = author_info.json()["docs"]
    all_books = []
    #print(author_books)
    print("here")
    book_titles = []
    for i in author_books:
        #print(i)
        book = requests.get(f"https://openlibrary.org/{i['key']}.json").json()
        if not book["title"] in book_titles:
            book_titles.append(book["title"])
            all_books.append(book["key"])
            #all_books.append({book["title"]: book["key"]})


        # if all_books:
        #     for j in all_books:
        #         if j["title"] == book["title"]:
        #             continue
        #     all_books.append(book)

    # for i in all_books:
    #     print(i)
    #     print("-------------------------")
    #print(all_books)
    print("all keys got")
    return all_books


def search_info_by_category(category):
    author_info = requests.get(f"https://openlibrary.org/search.json?author={author}&limit=5")
    author_books = author_info.json()["docs"]
    all_books = []
    #print(author_books)
    print("here")
    book_titles = []
    for i in author_books:
        #print(i)
        book = requests.get(f"https://openlibrary.org/{i['key']}.json").json()
        if not book["title"] in book_titles:
            book_titles.append(book["title"])
            all_books.append(book["key"])
            #all_books.append({book["title"]: book["key"]})


        # if all_books:
        #     for j in all_books:
        #         if j["title"] == book["title"]:
        #             continue
        #     all_books.append(book)

    # for i in all_books:
    #     print(i)
    #     print("-------------------------")
    #print(all_books)
    print("all keys got")
    return all_books
