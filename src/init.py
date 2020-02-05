from flask import Flask, redirect, render_template, url_for

try:
    import src.local_config as config
except ImportError:
    import src.config as config

app = Flask(__name__)

from src.modules.auth_module.auth import auth

app.register_blueprint(auth)


@app.route("/")
def index():
    return redirect(url_for("auth.login"))


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
