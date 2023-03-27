from flask import Flask, render_template, request

app = Flask(__name__)

app.secret_key = "Someurj"


@app.route("/", methods=["GET", "POST"])
def index():
    print(request.data)
    return render_template("index.html")