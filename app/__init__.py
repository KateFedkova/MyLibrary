from flask import Flask, render_template, request, make_response
from werkzeug.security import generate_password_hash

from .database import Users, session
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.secret_key = "Someurj"


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#     return render_template("index.html")

from app import endpoints
