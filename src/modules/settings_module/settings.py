from flask import Blueprint

from src.lib import (
    get_current_user,
    render,
)
from src.models import Subject

settings = Blueprint("settings", __name__, template_folder="templates")


@settings.route("/settings")
def settings_page():
    return render(
        "settings.html",
        title="Настройки",
        header_label="Настройки",
        current_subj="russian",
        subject_list=[],
        user_math_type=0
    )
