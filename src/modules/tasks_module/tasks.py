from flask import Blueprint

from src.lib import render, count_percentage_on_task, get_status_on_task
from src.models import Subject, TaskType

tasks = Blueprint("tasks", __name__, template_folder="templates")


@tasks.route("/<subj_name>/<mode_name>")
def app_logged_in(subj_name, mode_name):
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
                    "status": get_status_on_task(t)
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
