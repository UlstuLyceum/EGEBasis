import hashlib

from flask import render_template, session

from src.models import Task, TaskLink, TaskTypeLink, User

try:
    import src.local_config as config
except ImportError:
    import src.config as config


def render(template_name, **kwargs):
    return render_template(template_name, current_user=get_current_user(), **kwargs)


def get_current_user():
    email = session.get("email", None)
    password = session.get("password", None)
    user = User.find_one({"email": email, "password": password})
    return user


def hash_password(raw_data):
    m = hashlib.md5()
    m.update((config.SALT + raw_data).encode("utf-8"))
    return m.hexdigest()


def generate_confirm_code(email):
    return hash_password(email)[:10]


def count_percentage_on_task(tasktype):
    user = get_current_user()
    related_tasks = Task.find({"task_type": tasktype.id})
    done_tasks = 0
    for task in related_tasks:
        done_tasks += TaskLink.find(
            {"done": True, "task": task.id, "user": user.id}
        ).count()
    all_tasks = related_tasks.count()
    if all_tasks == 0:
        print("No tasks found for task type " + tasktype.number)
        return 0
    return int(done_tasks / all_tasks * 100)


def get_status_on_task(tasktype):
    user = get_current_user()
    res = TaskTypeLink.find_one({"task_type": tasktype.id, "user": user.id})
    if not res:
        return 0
    return res.status
