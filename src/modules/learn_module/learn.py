from flask import Blueprint, abort, redirect, url_for
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
        "5.4",
        "5.5",
        "5.6",
        "5.7",
        "5.8",
        "5.9",
        "5.10",
        "5.11",
        "5.12",
        "5.13",
        "5.14",
        "6.1",
        "6.2",
        "6.3",
        "6.4",
        "6.5",
        "6.6",
        "6.7",
        "6.8",
        "6.9",
        "6.10",
        "6.11",
        "6.12",
        "6.13",
        "6.14",
        "6.15",
        "6.16",
        "6.17",
        "7.1",
        "7.2",
        "7.3",
        "7.4",
        "7.5",
        "7.6",
        "7.7",
        "7.8",
        "7.9",
        "7.10",
        "7.11",
        "7.12",
        "7.13",
        "7.14",
        "7.15",
        "7.16",
        "7.17",
        "7.18",
        "7.19",
        "8.1",
        "8.2",
        "8.3",
        "8.4",
        "8.5",
        "8.6",
        "9.1",
        "9.2",
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
    if subj_name not in [sub["name"] for sub in subject_list]:
        abort(404)
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
