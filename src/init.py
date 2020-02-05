from flask import Flask, redirect, render_template, url_for
from flask_mail import Mail

from src.lib import get_current_user

try:
    import src.local_config as config
except ImportError:
    import src.config as config

app = Flask(__name__)

# Flask config
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['MAIL_SERVER'] = config.MAIL_SERVER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD

# Flask Mail
mail = Mail(app)

from src.modules.auth_module.auth import auth

app.register_blueprint(auth)


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
            subject_list=[
                {"label": "Русский", "name": "russian"},
                {"label": "Математика", "name": "math"},
                {"label": "Информатика", "name": "it"},
            ],
        )
