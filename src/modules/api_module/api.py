from bson.objectid import ObjectId
from flask import Blueprint, request

from src.lib import count_percentage_on_task, get_current_user
from src.models import Subject, Task, TaskLink, TaskType, TaskTypeLink

api = Blueprint("api", __name__)


@api.route("/api/change_status", methods=["POST"])
def change_status():
    user = get_current_user()
    if user is None:
        return "No user context"
    subject_name = request.form["subject_name"]
    task_number = str(request.form["task_number"])
    new_status = int(request.form["new_status"])
    subject = Subject.find_one({"name": subject_name})
    tasktype = TaskType.find_one({"subject": subject.id, "number": task_number})
    tasktypelink = TaskTypeLink.find_one({"user": user.id, "task_type": tasktype.id})
    if not tasktypelink:
        tasktypelink = TaskTypeLink(
            user=user.id, task_type=tasktype.id, status=new_status
        )
    else:
        tasktypelink.status = new_status
    tasktypelink.commit()
    return "Query ok"


@api.route("/api/task_done", methods=["POST"])
def task_done():
    user = get_current_user()
    if user is None:
        return "No user context"
    task_id = request.form["task_id"]
    task = Task.find_one({"id": ObjectId(task_id)})
    tasklink = TaskLink.find_one({"user": user.id, "task": task.id, "done": True})
    if tasklink is not None:
        return "Task already done"
    tasktype = task.task_type.fetch()
    tasktypelink = TaskTypeLink.find_one({"user": user.id, "task_type": tasktype.id})
    if tasktypelink is not None:
        tasktypelink.done_tasks += 1
    else:
        tasktypelink = TaskTypeLink(
            task_type=tasktype, user=user, done_tasks=0, status=0
        )
    tasktypelink.commit()
    tasklink = TaskLink(user=user, task=task, done=True)
    tasklink.commit()
    return "Query ok"


@api.route("/api/get_percentage", methods=["POST"])
def get_percentage():
    user = get_current_user()
    if user is None:
        return "No user context"
    subj_name = request.form["subj_name"]
    number = request.form["number"]
    subject = Subject.find_one({"name": subj_name})
    tasktype = TaskType.find_one({"subject": subject.id, "number": str(number)})
    return count_percentage_on_task(tasktype)
