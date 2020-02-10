from flask import Blueprint, request, url_for
from werkzeug.utils import redirect

from src.lib import get_current_user, hash_password, render
from src.models import Subject

settings = Blueprint("settings", __name__, template_folder="templates")


@settings.route("/settings", methods=["GET", "POST"])
def settings_page():
    user = get_current_user()
    if user is None:
        return redirect(url_for("index"))
    user_math_type = int(not user.is_math_basic)
    if request.method == "GET":
        return render(
            "settings.html",
            title="Настройки",
            header_label="Настройки",
            current_subj="russian",
            subject_list=[],
            user_math_type=user_math_type,
        )
    oldpass = request.form["oldpass"]
    newpass = request.form["newpass"]
    math_type = int(request.form["math_type"])
    print(oldpass, newpass, math_type)
    if not oldpass:
        user.is_math_basic = not bool(math_type)
        user.commit()
        return render(
            "settings.html",
            title="Настройки",
            header_label="Настройки",
            current_subj="russian",
            subject_list=[],
            user_math_type=math_type,
            ok=True,
        )
    if hash_password(oldpass) != user.password:
        return render(
            "settings.html",
            title="Настройки",
            header_label="Настройки",
            current_subj="russian",
            subject_list=[],
            user_math_type=user_math_type,
            bad_password=True,
        )
    user.password = hash_password(newpass)
    user.is_math_basic = not bool(math_type)
    user.commit()
    return render(
        "settings.html",
        title="Настройки",
        header_label="Настройки",
        current_subj="russian",
        subject_list=[],
        user_math_type=math_type,
        ok=True,
    )
