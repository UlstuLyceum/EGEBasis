from flask import Flask, redirect, render_template, url_for
from flask_mail import Mail

from src.lib import get_current_user

try:
    import src.local_config as config
except ImportError:
    import src.config as config

app = Flask(__name__)

# Flask config
app.config["SECRET_KEY"] = config.SECRET_KEY
app.config["MAIL_SERVER"] = config.MAIL_SERVER
app.config["MAIL_PORT"] = config.MAIL_PORT
app.config["MAIL_USE_TLS"] = config.MAIL_USE_TLS
app.config["MAIL_USERNAME"] = config.MAIL_USERNAME
app.config["MAIL_DEFAULT_SENDER"] = config.MAIL_DEFAULT_SENDER
app.config["MAIL_PASSWORD"] = config.MAIL_PASSWORD

# Flask Mail
mail = Mail(app)

from src.modules.auth_module.auth import auth

app.register_blueprint(auth)


subject_list = [
    {"label": "Русский", "name": "russian"},
    {"label": "Математика", "name": "math"}
]

tasks_list = [
    {"number": 1, "compete_percentage": 100, "points": 1, "status": 3},
    {"number": 2, "compete_percentage": 47, "points": 1, "status": 1},
    {"number": 3, "compete_percentage": 70, "points": 1, "status": 1},
    {"number": 4, "compete_percentage": 34, "points": 1, "status": 2},
    {"number": 5, "compete_percentage": 28, "points": 1, "status": 1},
    {"number": 6, "compete_percentage": 82, "points": 1, "status": 3},
    {"number": 7, "compete_percentage": 56, "points": 1, "status": 3},
    {"number": 8, "compete_percentage": 27, "points": 5, "status": 1},
    {"number": 9, "compete_percentage": 72, "points": 1, "status": 3},
    {"number": 10, "compete_percentage": 64, "points": 1, "status": 2},
    {"number": 11, "compete_percentage": 25, "points": 1, "status": 1},
    {"number": 12, "compete_percentage": 46, "points": 1, "status": 0},
    {"number": 13, "compete_percentage": 35, "points": 1, "status": 1},
    {"number": 14, "compete_percentage": 67, "points": 1, "status": 2},
    {"number": 15, "compete_percentage": 43, "points": 1, "status": 2},
    {"number": 16, "compete_percentage": 37, "points": 2, "status": 1},
    {"number": 17, "compete_percentage": 96, "points": 1, "status": 2},
    {"number": 18, "compete_percentage": 66, "points": 1, "status": 3},
    {"number": 19, "compete_percentage": 24, "points": 1, "status": 1},
    {"number": 20, "compete_percentage": 63, "points": 1, "status": 0},
    {"number": 21, "compete_percentage": 67, "points": 1, "status": 1},
    {"number": 22, "compete_percentage": 35, "points": 1, "status": 2},
    {"number": 23, "compete_percentage": 74, "points": 1, "status": 3},
    {"number": 24, "compete_percentage": 35, "points": 1, "status": 0},
    {"number": 25, "compete_percentage": 26, "points": 1, "status": 1},
    {"number": 26, "compete_percentage": 27, "points": 4, "status": 0}
]


@app.route("/")
def index():
    user = get_current_user()
    if user is None:
        return redirect(url_for("auth.login"))
    return redirect(url_for("app_logged_in", subj_name="russian", mode_name="tasks"))


@app.route("/<subj_name>/<mode_name>")
def app_logged_in(subj_name, mode_name):
    if mode_name == "tasks":
        return render_template(
            "tasks.html",
            title="Задания",
            header_label="Все задания первой части",
            current_subj=subj_name,
            current_mode=mode_name,
            subject_list=subject_list,
            tasks_list=tasks_list,
        )
