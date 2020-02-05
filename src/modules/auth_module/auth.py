from flask import Blueprint, request, session, url_for
from werkzeug.utils import redirect

from src.lib import render, hash_password, get_current_user
from src.models import User

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if get_current_user() is not None:
        return redirect(url_for("index"))
    if request.method == "GET":
        return render("login.html", title="Войти")
    email = request.form["email"]
    raw_password = request.form["password"]
    password = hash_password(raw_password)
    user = User.find_one({"email": email, "password": password})
    if user:
        session["email"] = email
        session["password"] = password
        return redirect(url_for("index"))
    return render("login.html", title="Войти", error=True)


@auth.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("password", None)
    return redirect(url_for("auth.login"))


@auth.route("/signup")
def signup():
    return render("signup.html", title="Зарегистрироваться")
