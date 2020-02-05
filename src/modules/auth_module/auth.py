from flask import Blueprint

from src.lib import render

auth = Blueprint("auth", __name__, template_folder="templates")


@auth.route("/login")
def login():
    return render("login.html", title="Войти")


@auth.route("/signup")
def signup():
    return render("signup.html", title="Зарегистрироваться")
