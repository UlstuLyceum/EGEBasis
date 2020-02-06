from flask import Blueprint, request

from src.lib import get_current_user
from src.models import Subject, TaskType, TaskTypeLink

api = Blueprint("api", __name__)


@api.route('/api/change_status', methods=["POST"])
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
        tasktypelink = TaskTypeLink(user=user.id, task_type=tasktype.id, status=new_status)
    else:
        tasktypelink.status = new_status
    tasktypelink.commit()
    return 'Query ok'


@api.route('/api/task_done', methods=["POST"])
def task_done():
    user = get_current_user()
    if user is None:
        return "No user context"
    # TODO process
    return "Query ok"
