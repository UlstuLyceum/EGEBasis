from flask import Blueprint, url_for
from werkzeug.utils import redirect

from src.lib import get_current_user, render
from src.models import Subject

learn = Blueprint("learn", __name__, template_folder="templates")

subject = {
    "label": "russian",
    "cod_amount": "11",
    "cods": [
        "1.1",
        "1.2",
        "2.1",
        "2.2",
        "2.3",
        "2.4",
        "2.5",
        "3.1",
        "3.2",
        "3.3",
        "3.4",
        "4.1",
        "4.2",
        "4.3",
        "5.1",
        "5.2",
        "5.3",
        "9.3",
        "9.4",
        "10.1",
        "10.2",
        "10.3",
        "10.4",
        "10.5",
        "11",
    ],
}
subject["cods"] = list(
    map(lambda x: x.replace(".", "-") if "." in x else x, subject["cods"])
)


@learn.route("/<subj_name>/learn")
def app_logged_in(subj_name):
    if get_current_user() is None:
        return redirect(url_for("index"))
    subject_list = list(Subject.find({"hidden": False}))
    return render(
        "learn.html",
        title="Теория",
        header_label="Вся теория по кодификаторам",
        current_subj=subj_name,
        current_mode="learn",
        subject_list=subject_list,
        cod_amount=11,
        cods=subject["cods"],
    )
