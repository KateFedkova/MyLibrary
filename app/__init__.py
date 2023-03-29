from flask import Flask
from .database import Users, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.secret_key = "Someurj"
app.config["JWT_SECRET_KEY"] = "skiejdm"
CORS(app)
JWTManager(app)


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         username = request.form["username"]
#         password = request.form["password"]
#     return render_template("index.html")

from app import endpoints
