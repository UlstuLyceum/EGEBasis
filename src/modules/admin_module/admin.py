from bson.objectid import ObjectId
from flask import Blueprint, request

from src.lib import get_current_user, render
from src.models import Subject, Task, TaskType

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/admin", methods=["GET", "POST"])
def admin_main():
    user = get_current_user()
    if user is None:
        return render("access-denied.html")
    if not user.is_admin:
        return render("access-denied.html")
    subjects = Subject.find({"hidden": False})
    if request.method == "GET":
        return render("add-task.html", subjects=subjects)
    subject = Subject.find_one({"label": request.form["subject"]})
    task_type = TaskType.find_one(
        {"number": request.form["task_type"], "subject": subject.id}
    )
    description = request.form["description"]
    var1 = request.form["var1"]
    var2 = request.form["var2"]
    var3 = request.form["var3"]
    var4 = request.form["var4"]
    var5 = request.form["var5"]
    options = []
    if var1:
        options.append(var1)
    if var2:
        options.append(var2)
    if var3:
        options.append(var3)
    if var4:
        options.append(var4)
    if var5:
        options.append(var5)
    answers = request.form["answers"].replace(" ", "").split(",")
    explanation = request.form["explanation"]
    task = Task(
        task_type=task_type,
        description=description,
        options=options,
        answers=answers,
        explanation=explanation,
        text=ObjectId("5e4066a91c9d440000785ec1"),
    )
    task.commit()
    return render("add-task.html", subjects=subjects, ok=True)
