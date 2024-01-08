import os
import ast
from flask import Flask, render_template, session, redirect, request, url_for
from dotenv import load_dotenv
from pygments import highlight
from pygments.styles import get_all_styles
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.lexers import get_all_lexers
from PIL import ImageColor
import base64
from utils import take_screenshot_from_url


app = Flask(__name__)

DEFAULT_STYLE = "monokai"
DEFAULT_LANGUAGE = ("Detect language (Automatic)", "auto")


# Load secret_key from environment variable, in order to be able to use sessions safely.
load_dotenv()
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY")


# This is the main endpoint for the app.
@app.route("/", methods=["GET"])
def code():
    all_languages = list(get_all_lexers())
    all_languages.insert(0, DEFAULT_LANGUAGE)

    if session.get("code") is None:
        session["code"] = ""
    if session.get("language") is None:
        session["language"] = DEFAULT_LANGUAGE

    lines = session["code"].split("\n")

    context = {
        "message": "Code to image converter",
        "code": session["code"],
        "all_languages": all_languages,
        "selected_language": session["language"],
        "num_lines": len(lines),
        "max_chars": len(max(lines, key=len)),
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


# Function to check if the background color is dark
def is_dark_background(color):
    rgb = ImageColor.getcolor(color, "RGB")
    luminance = (0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]) / 255.0
    return luminance < 0.5


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

    # Get the selected style and background color
    selected_style = session["style"]
    formatter = HtmlFormatter(style=selected_style)
    style_bg_color = formatter.style.background_color

    # Check if the background is dark
    is_dark_theme = is_dark_background(style_bg_color)

    # Set text color based on theme
    text_color = "white" if is_dark_theme else "black"

    context = {
        "message": message,
        "all_styles": list(get_all_styles()),
        "selected_style": selected_style,
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": style_bg_color,
        "highlighted_code": highlight(session["code"], lexer, formatter),
        "text_color": text_color,
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


@app.route("/image", methods=["GET"])
def image():
    session_data = {
        "name": app.config["SESSION_COOKIE_NAME"],
        "value": request.cookies.get(app.config["SESSION_COOKIE_NAME"]),
        "url": request.host_url,
    }
    target_url = request.host_url + url_for("style")
    image_bytes = take_screenshot_from_url(target_url, session_data)
    context = {
        "message": "Done! 🎉",
        "image_b64": base64.b64encode(image_bytes).decode("utf-8"),
    }
    return render_template("image.html", **context)
