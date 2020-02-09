from flask import Blueprint, redirect, url_for

from src.lib import (
    get_current_user,
    render,
)
from src.models import Subject

settings = Blueprint("settings", __name__, template_folder="templates")


@settings.route("/settings")
def settings_page():
    if get_current_user() is None:
        return redirect(url_for("index"))
    return render(
        "settings.html",
        title="Настройки",
        header_label="Настройки",
        current_subj="russian",
        subject_list=[],
        user_math_type=0
    )
