import os
from flask import Flask, render_template, session, redirect, request, url_for
from dotenv import load_dotenv

app = Flask(__name__)

# Load secret_key from environment variable, in order to be able to use sessions safely.
load_dotenv()
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")


# This is the main endpoint for the app.
@app.route("/", methods=["GET"])
def code():
    if session.get("code") is None:
        session["code"] = ""
    context = {
        "message": "Code to image converter",
        "code": session["code"],
    }
    return render_template("code_input.html", **context)


@app.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code")
    return redirect(url_for("code"))


@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = ""
    return redirect(url_for("code"))
