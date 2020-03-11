from flask import Blueprint, request, session, url_for
from flask_mail import Message
from werkzeug.utils import redirect
import random

from src.init import mail
from src.lib import generate_confirm_code, get_current_user, hash_password, render
from src.models import User

auth = Blueprint("auth", __name__, template_folder="templates")

try:
    import src.local_config as config
except ImportError:
    import src.config as config


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
        if not user.confirm_code:
            session["email"] = email
            session["password"] = password
            return redirect(url_for("index"))
        return render("login.html", title="Войти", not_confirmed=True)
    return render("login.html", title="Войти", error=True)


@auth.route("/logout")
def logout():
    session.pop("email", None)
    session.pop("password", None)
    return redirect(url_for("auth.login"))


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render("signup.html", title="Зарегистрироваться")
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    if User.find_one({"email": email}) is not None:
        return render("signup.html", title="Зарегистрироваться", user_exists=True)
    confirm_code = generate_confirm_code(email)
    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        confirm_code=confirm_code,
    )
    user.commit()
    msg = Message(
        subject="Подтверждение аккаунта",
        sender=config.MAIL_DEFAULT_SENDER,
        recipients=[email],
        body="Ваша ссылка для подтверждения: "
        + config.APP_URL
        + url_for("auth.confirm", confirm_code=confirm_code)[1:],
    )
    mail.send(msg)
    return render("finishSignup.html", title="Завершение регистрации")


@auth.route("/confirm/<confirm_code>")
def confirm(confirm_code):
    user = User.find_one({"confirm_code": confirm_code})
    if not user:
        return redirect(url_for("index"))
    user.confirm_code = ""
    user.commit()
    return redirect(url_for("auth.login"))


@auth.route("/reset", methods=["POST"])
def reset():
    email = request.form["reestablishEmail"]
    user = User.find_one({"email": email})
    if user is None:
        return "Пользователя с таким email не существует"
    confirm_code = generate_confirm_code(email + str(random.randint(0, 10000)))
    user.reset_code = confirm_code
    user.commit()
    msg = Message(
        subject="Восстановление пароля",
        sender=config.MAIL_DEFAULT_SENDER,
        recipients=[email],
        body="Ваша ссылка для подтверждения: "
        + config.APP_URL
        + url_for("auth.reset_finish", confirm_code=confirm_code)[1:],
    )
    mail.send(msg)
    return "Ссылка отправлена на почту"


@auth.route("/reset/<confirm_code>", methods=["GET", "POST"])
def reset_finish(confirm_code):
    user = User.find_one({"reset_code": confirm_code})
    if user is None:
        return "Код на восстановление пароля недействителен"
    if request.method == "GET":
        return render("acceptReset.html", confirm_code=confirm_code)
    password = request.form["password"]
    rpassword = request.form["rpassword"]
    if password != rpassword:
        return "Несовпадающие пароли"
    user.password = hash_password(password)
    user.confirm_code = ""
    user.commit()
    return redirect(url_for("index"))
