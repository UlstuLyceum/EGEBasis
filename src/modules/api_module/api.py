from flask import Blueprint, request

api = Blueprint("api", __name__)


@api.route('/api/change_status', methods=["POST"])
def change_status():
    subject_name = request["subject_name"]
    task_number = str(request["task_number"])
    new_status = int(request["new_status"])
    print(subject_name, task_number, new_status)
    return 'Query ok'
