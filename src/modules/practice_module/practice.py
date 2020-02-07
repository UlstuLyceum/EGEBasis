from random import choice

from bson.objectid import ObjectId
from flask import Blueprint, request, session, url_for
from werkzeug.utils import redirect

from src.lib import get_current_user, render
from src.models import Subject, Task, TaskType

practice = Blueprint("practice", __name__, template_folder="templates")


@practice.route("/<subj_name>/practice")
def app_logged_in(subj_name):
    user = get_current_user()
    if user is None:
        return redirect(url_for("index"))
    exclude = request.args.get("exclude", "").split()
    subject = Subject.find_one({"name": subj_name})
    task_types = TaskType.find({"subject": subject.id})
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
    return render("test.html", tasks=tasks, current_subj=subj_name)


@practice.route("/<subj_name>/results", methods=["POST"])
def results(subj_name):
    user = get_current_user()
    if user is None:
        return redirect(url_for("index"))
    tasks = []
    right = 0
    all = 0
    for q in request.form:
        number = q[4:]
        answer = request.form[q]
        all += 1
        task = Task.find_one({"id": ObjectId(session[q])})
        tasks.append(
            {
                "number": number,
                "user_answer": answer,
                "right_answer": list(task.answers),
            }
        )
        if answer in task.answers:
            right += 1
    return render(
        "results.html", current_subj=subj_name, tasks=tasks, right=right, all=all
    )
