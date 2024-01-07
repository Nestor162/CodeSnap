import os
import ast
from flask import Flask, render_template, session, redirect, request, url_for
from dotenv import load_dotenv
from pygments import highlight
from pygments.styles import get_all_styles
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.lexers import get_all_lexers


app = Flask(__name__)

DEFAULT_STYLE = "monokai"
DEFAULT_LANGUAGE = ("Detect language (Automatic)", "auto")


# Load secret_key from environment variable, in order to be able to use sessions safely.
load_dotenv()
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")


# This is the main endpoint for the app.
@app.route("/", methods=["GET"])
def code():
    if session.get("code") is None:
        session["code"] = ""
    if session.get("language") is None:
        session["language"] = DEFAULT_LANGUAGE
    context = {
        "message": "Code to image converter",
        "code": session["code"],
        "all_languages": list(get_all_lexers()),
        "selected_language": session["language"],
    }
    return render_template("code_input.html", **context)


# Endpoint for saving the code to the session.
# @app.route("/save_code", methods=["POST"])
# def save_code():
#     session["code"] = request.form.get("code")
#     session["selected_language"] = request.form.get("selected_language")
#     return redirect(url_for("code"))


# Endpoint for resetting the session.
@app.route("/reset_session", methods=["POST"])
def reset_session():
    session.clear()
    session["code"] = ""
    return redirect(url_for("code"))


# Function that iterates through all the lexers aliases and returns the first one that matches the code.
def get_lexer_by_name_or_aliases(aliases, code):
    # Convert the string to a tuple of aliases.
    aliases = ast.literal_eval(aliases)
    for alias in aliases:
        try:
            lexer = get_lexer_by_name(alias, stripall=True)
            return lexer
        except ValueError:
            pass

    # If none of the aliases matched, try to guess the lexer.
    try:
        lexer = guess_lexer(code)
        return lexer
    except:
        return None


# Endpoint for the style selection page.
@app.route("/style", methods=["GET"])
def style():
    if session.get("style") is None:
        session["style"] = DEFAULT_STYLE

    selected_language = session["language"]
    detected_language = ""

    # If the language is "Detect language (Automatic)", then we need to guess the lexer.
    if selected_language[1] == "auto":
        detected_language = guess_lexer(session["code"]).name.capitalize()
        message = f"Select your style for your {detected_language} code 🎨"
        lexer = guess_lexer(session["code"])
    else:
        detected_language = selected_language[0].capitalize()
        message = f"Select your style for your {detected_language} code 🎨"
        lexer = get_lexer_by_name_or_aliases(selected_language[1], session["code"])

    formatter = HtmlFormatter(style=session["style"])
    context = {
        "message": message,
        "all_styles": list(get_all_styles()),
        "selected_style": session["style"],
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": formatter.style.background_color,
        "highlighted_code": highlight(session["code"], lexer, formatter),
    }
    return render_template("style_selection.html", **context)


# Endpoint for saving the style to the session.
@app.route("/save_style", methods=["POST"])
def save_style():
    if request.form.get("style") is not None:
        session["style"] = request.form.get("style")
    if request.form.get("code") is not None:
        session["code"] = request.form.get("code")
    if request.form.get("language") is not None:
        selected_language_str = request.form.get("language")
        selected_language = tuple(selected_language_str.split("|"))
        session["language"] = selected_language
    return redirect(url_for("style"))
