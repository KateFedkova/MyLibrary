import requests


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
