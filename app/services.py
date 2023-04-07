import requests
import json
from .database import session


def add_user(obj_to_add):
    session.add(obj_to_add)
    session.commit()


def convert_obj_to_str(obj_to_convert, time=None):
    converted = obj_to_convert.__dict__
    converted.pop('_sa_instance_state', None)
    if time:
        converted["date_added"] = converted["date_added"].strftime("%H:%M %d-%m-%Y")
    json_dict = json.dumps(converted)
    return json_dict


def search_info_by_title(title):
    books = requests.get(f"https://openlibrary.org/search.json?title={title}")
    book_key = books.json()["docs"][0]["key"]
    info_book = requests.get(f"https://openlibrary.org/{book_key}.json").json()
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
    try:
        subject_times = info_book["subject_times"]
    except KeyError:
        subject_times = "No subject times found"

    return description, subject_places, subjects, subject_times


def search_info_by_author(author):
    author_info = requests.get(f"https://openlibrary.org/search.json?author={author}&limit=5")
    author_books = author_info.json()["docs"]
    all_books = []

    book_titles = []
    for i in author_books:

        book = requests.get(f"https://openlibrary.org/{i['key']}.json").json()
        if not book["title"] in book_titles:
            book_titles.append(book["title"])
            all_books.append(book["key"])

    return all_books


def search_info_by_category(category):
    all_books_by_category = requests.get(f"https://openlibrary.org/subjects/{category}.json?limit=10")
    books_by_category = all_books_by_category.json()["works"]
    all_books = []

    book_titles = []
    for i in books_by_category:
        book = requests.get(f"https://openlibrary.org/{i['key']}.json").json()
        if not book["title"] in book_titles:
            book_titles.append(book["title"])
            all_books.append(book["key"])

    return all_books


def book_info(book_key):
    book_info = []
    for key in book_key:
        info_book = requests.get(f"https://openlibrary.org/{key}.json").json()

        title = info_book["title"]

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

        try:
            subject_times = info_book["subject_times"]
        except KeyError:
            subject_times = "No subject times found"

        response_dict = {"title": title, "description": description, "subject_places": subject_places,
                         "subjects": subjects, "subject_times": subject_times}

        book_info.append(response_dict)

    return book_info