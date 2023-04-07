from flask import Flask
from .database import Users, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from environs import Env

env = Env()
env.read_env()

app = Flask(__name__)

app.secret_key = env.str("SECRET_KEY")
app.jwt_secret_key = env.str("JWT_SECRET_KEY")
CORS(app)
JWTManager(app)

from app import endpoints
