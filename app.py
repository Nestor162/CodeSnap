import os
from flask import Flask, render_template, session, redirect, request, url_for
from dotenv import load_dotenv
from pygments import highlight
from pygments.styles import get_all_styles
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer

app = Flask(__name__)

DEFAULT_STYLE = "monokai"

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


# Endpoint for saving the code to the session.
@app.route("/save_code", methods=["POST"])
def save_code():
    session["code"] = request.form.get("code")
    return redirect(url_for("code"))


# Endpoint for resetting the session.
@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = ""
    return redirect(url_for("code"))


# Endpoint for the style selection page.
@app.route("/style", methods=["GET"])
def style():
    if session.get("style") is None:
        session["style"] = DEFAULT_STYLE
    formatter = HtmlFormatter(style=session["style"])
    context = {
        "message": "Select Your Style 🎨",
        "all_styles": list(get_all_styles()),
        "selected_style": session["style"],
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": formatter.style.background_color,
        "highlighted_code": highlight(session["code"], Python3Lexer(), formatter),
    }
    return render_template("style_selection.html", **context)


# Endpoint for saving the style to the session.
@app.route("/save_style", methods=["POST"])
def save_style():
    session["style"] = request.form.get("style")
    return redirect(url_for("style"))
