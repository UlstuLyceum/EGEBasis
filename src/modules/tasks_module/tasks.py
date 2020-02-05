from flask import Blueprint, url_for
from werkzeug.utils import redirect

from src.lib import count_percentage_on_task, get_status_on_task, render, get_current_user
from src.models import Subject, TaskType, Task

tasks = Blueprint("tasks", __name__, template_folder="templates")


@tasks.route("/<subj_name>/<mode_name>")
def app_logged_in(subj_name, mode_name):
    if get_current_user() is None:
        return redirect(url_for("index"))
    if mode_name == "tasks":
        subject_list = list(Subject.find({"hidden": False}))
        subject = Subject.find_one({"name": subj_name})
        tasks_list = []
        raw_tasks = TaskType.find({"subject": subject.id})
        for t in raw_tasks:
            tasks_list.append(
                {
                    "number": int(t.number),
                    "compete_percentage": count_percentage_on_task(t),
                    "points": t.points,
                    "status": get_status_on_task(t),
                }
            )
        return render(
            "tasks.html",
            title="Задания",
            header_label="Все задания первой части",
            current_subj=subj_name,
            current_mode=mode_name,
            subject_list=subject_list,
            tasks_list=tasks_list,
        )
    return "No such page"


@tasks.route('/<subj_name>/task/<int:task_id>')
def task_theory(subj_name, task_id):
    return render("task-theory.html", current_subj=subj_name, task_id=task_id)


@tasks.route('/<subj_name>/task/<int:task_id>/tasks')
def task_tasks(subj_name, task_id):
    if get_current_user() is None:
        return redirect(url_for("index"))
    user = get_current_user()
    subject = Subject.find_one({"name": subj_name})
    task_type = TaskType.find_one({"subject": subject.id, "number": str(task_id)})
    tasks = []
    raw_tasks = Task.find({"task_type": task_type.id})
    for task in raw_tasks:
        tasks.append({
            "body": "Тут содержание задания",
            "text": None,  # связанный с заданием текст
            "done": True,
            "answer": "123"
        })
    return render("task-list.html", current_subj=subj_name, tasks=tasks)
