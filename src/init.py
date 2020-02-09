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
from src.modules.tasks_module.tasks import tasks
from src.modules.learn_module.learn import learn
from src.modules.practice_module.practice import practice
from src.modules.settings_module.settings import settings
from src.modules.api_module.api import api
from src.modules.admin_module.admin import admin

app.register_blueprint(auth)
app.register_blueprint(tasks)
app.register_blueprint(learn)
app.register_blueprint(practice)
app.register_blueprint(settings)
app.register_blueprint(api)
app.register_blueprint(admin)


@app.route("/")
def index():
    user = get_current_user()
    if user is None:
        return redirect(url_for("auth.login"))
    return redirect(url_for("tasks.app_logged_in", subj_name="russian"))
