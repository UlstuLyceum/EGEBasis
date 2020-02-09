import time
from random import choice

import flask
from bson.objectid import ObjectId
from flask import Blueprint, abort, request, session, url_for
from werkzeug.utils import redirect

from src.lib import get_current_user, render
from src.models import Subject, Task, TaskLink, TaskType

practice = Blueprint("practice", __name__, template_folder="templates")


@practice.route("/<subj_name>/practice")
def app_logged_in(subj_name):
    user = get_current_user()
    if user is None:
        return redirect(url_for("index"))
    exclude = request.args.get("exclude", "").split()
    subject = Subject.find_one({"name": subj_name})
    task_types = TaskType.find({"subject": subject.id})
    subject_list = list(Subject.find({"hidden": False}))
    tasks = []
    for tt in task_types:
        if tt.number in exclude:
            continue
        rel_tasks = Task.find({"task_type": tt.id})
        task = choice(list(rel_tasks))
        session["task" + str(tt.number)] = str(task.id)
        text = None
        if task.text.pk is not None:
            text = task.text.fetch().body
        tasks.append(
            {
                "number": tt.number,
                "description": eval('"' + task.description + '"'),
                "text": text,
                "options": task.options,
            }
        )
    return render(
        "practice.html",
        title="Тест",
        header_label="Тест в формате ЕГЭ",
        current_subj=subj_name,
        current_mode="practice",
        subject_list=subject_list,
        tasks=tasks,
    )


@practice.route("/<subj_name>/results", methods=["POST", "GET"])
def results(subj_name):
    if flask.request.method == "GET":
        abort(404)
    user = get_current_user()
    if user is None:
        return redirect(url_for("index"))
    tasks = []
    right = 0
    all = 0
    test_time = int(request.form["time_counter"])
    test_time = time.strftime("%H:%M:%S", time.gmtime(test_time))
    subject_list = list(Subject.find({"hidden": False}))
    first_points = 0
    for q in request.form:
        if q != "time_counter":
            number = q[4:]
            answer = request.form[q]
            all += 1
            task = Task.find_one({"id": ObjectId(session[q])})
            tl = TaskLink.find_one({"task": task.id, "user": user.id})
            text = None
            if task.text.pk is not None:
                text = task.text.fetch().body
            tasks.append(
                {
                    "user_answer": answer,
                    "number": number,
                    "description": eval('"' + task.description + '"'),
                    "text": text,
                    "options": task.options,
                    "done": tl.done if tl else False,
                    "answers": task.answers,
                    "explanation": task.explanation,
                }
            )
            if answer in task.answers:
                first_points += points[subj_name]["first"][int(number)]
                right += 1
    return render(
        "practice-results.html",
        title="Ответы на тест",
        header_label="Тест в формате ЕГЭ",
        current_subj=subj_name,
        current_mode="tasks",
        subject_list=subject_list,
        tasks=tasks,
        right=right,
        all=all,
        time=test_time,
        first_points=first_points,
        second_points=points[subj_name]["second"][first_points],
    )


points = {
    "russian": {
        "first": [
            0,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            5,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            2,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            4,
        ],
        "second": [
            0,
            3,
            5,
            8,
            10,
            12,
            15,
            17,
            20,
            22,
            24,
            26,
            28,
            30,
            32,
            34,
            36,
            38,
            39,
            40,
            41,
            43,
            44,
            45,
            46,
            48,
            49,
            50,
            51,
            53,
            54,
            55,
            56,
            57,
            59,
            60,
        ],
    }
}
