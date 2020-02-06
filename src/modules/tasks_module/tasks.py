from flask import Blueprint, url_for
from werkzeug.utils import redirect

from src.lib import (
    count_percentage_on_task,
    get_current_user,
    get_status_on_task,
    render,
)
from src.models import Subject, Task, TaskLink, TaskType

tasks = Blueprint("tasks", __name__, template_folder="templates")


@tasks.route("/<subj_name>/tasks")
def app_logged_in(subj_name):
    if get_current_user() is None:
        return redirect(url_for("index"))
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
    for t in raw_tasks:
        tasks_list.append(
            {"number": 1, "compete_percentage": 100, "points": 1, "status": 0,}
        )
    return render(
        "tasks.html",
        title="Задания",
        header_label="Все задания первой части",
        current_subj=subj_name,
        current_mode="tasks",
        subject_list=subject_list,
        tasks_list=tasks_list,
    )


@tasks.route("/<subj_name>/task/<int:task_id>")
def task_theory(subj_name, task_id):
    subject_list = list(Subject.find({"hidden": False}))
    return render(
        "task.html",
        title="Задание",
        header_label="Теория по заданию",
        current_subj=subj_name,
        current_mode="tasks",
        subject_list=subject_list,
        task_id=task_id,
        cods=["1.1", "1.2"],
        task_description="В задании нужно прочитать текст и выбрать варианты ответов, которые наиболее точно передают "
                         "его главную мысль. В данном задании всегда два варианта ответа. За правильный даётся один "
                         "первичный балл."
    )


@tasks.route("/<subj_name>/task/<int:task_id>/tasks")
def task_tasks(subj_name, task_id):
    if get_current_user() is None:
        return redirect(url_for("index"))
    user = get_current_user()
    subject = Subject.find_one({"name": subj_name})
    task_type = TaskType.find_one({"subject": subject.id, "number": str(task_id)})
    tasks = []
    raw_tasks = Task.find({"task_type": task_type.id})
    for task in raw_tasks:
        tl = TaskLink.find_one({"task": task.id, "user": user.id})
        text = None
        if task.text is not None:
            text = task.text.fetch().body
            print(text)
        tasks.append(
            {
                "body": eval('"' + task.body + '"'),
                "text": text,
                "done": tl.done if tl else False,
                "answer": task.answer,
            }
        )
    return render("task-list.html", current_subj=subj_name, tasks=tasks)
